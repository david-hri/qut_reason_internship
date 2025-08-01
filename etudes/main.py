from extract_facts import extract_facts_from_prompt, extract_entities_from_file
from extract_rules import *
from extract_queries import extract_conclusions

import pytholog as pl
from openai import OpenAI
import os

# ==== Configuration ====
API_KEY_FILE = "api_key.txt"
RULES_FILE = "rules.txt"
FACTS_FILE = "facts.txt"
QUERIES_FILE = "queries.txt"

MODEL = "gpt-4"
TEMPERATURE = 0.0  # pour benchmark, déterministe

# Constantes et prompt NBA
NBA_SYSTEM_PROMPT = "You are a helpful NBA team consultant."
NBA_USER_PROMPT_BASE = """
You are given rules in NBA Collective Bargaining Agreement and the information about some teams and players. Then you will be given a list of operations, each of which describes how some teams conduct some transaction. You should determine whether each operation complies with the given rules.
Assume :
* the Salary Cap for the prior (2023-24) Salary Cap Year is $136,000,000;
* the Average Player Salary for the prior (2023-24) Salary Cap Year is $9,700,000;
* the Salary Cap for the current (2024-25) NBA Salary Cap Year is $140,588,000;
* the Luxury Tax is $170,814,000;
* the First Apron Level is $178,132,000;
* the Second Apron Level is $188,931,000;
* the Team Salary of each team listed under "Team Situations :" do not include the amount of contracts that expire at the end of 2023-2024 Salary Cap Year.

Reference Rules in NBA Collective Bargaining Agreement :
< reference_rules >

Decide whether any operation by any team violate the rules :
< user_query >

Analyze the described operations and explicitly state the type of Salary Cap Exceptions if you think the exception should be involved. Conclude your response with :
* "Answer : False." if there is no violation to the rules;
* "Answer : True. Illegal Operation : X. Problematic Team : Y." if Team Y in Operation X violates the rules.
Both X and Y should be a single capital letter as A / B / C /...
Your response :
"""

# ==== Fonctions utilitaires ====

def load_api_key(filepath):
    with open(filepath, "r") as f:
        return f.read().strip()

def read_file_strip_comments(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('%')]

def build_nba_description(operations_block, team_situations_block):
    """
    Construit la description utilisateur que on passe à extract_facts_from_prompt.
    operations_block : chaîne décrivant les opérations, ex "Operation A: ...\nOperation B:..."
    team_situations_block : chaîne décrivant les situations d'équipes (salaire, exceptions, etc.)
    """
    composed = f"""System Prompt: {NBA_SYSTEM_PROMPT}
User Prompt: You are a helpful NBA team consultant.
{operations_block}

Team Situations:
{team_situations_block}
"""
    return composed

def parse_llm_answer(answer_text):
    parsed = {
        "violation": None,
        "illegal_operation": None,
        "problematic_team": None,
        "raw": answer_text.strip()
    }
    if "Answer" in answer_text:
        if re_search := __import__('re').search(r'Answer\s*:\s*False\s*\.', answer_text, re.IGNORECASE):
            parsed["violation"] = False
            return parsed
        m = __import__('re').search(
            r'Answer\s*:\s*True\s*\.\s*Illegal Operation\s*:\s*([A-Z])\s*\.\s*Problematic Team\s*:\s*([A-Z])\s*\.',
            answer_text, re.IGNORECASE
        )
        if m:
            parsed["violation"] = True
            parsed["illegal_operation"] = m.group(1).upper()
            parsed["problematic_team"] = m.group(2).upper()
        else:
            if "True" in answer_text:
                parsed["violation"] = True
                io = __import__('re').search(r'Illegal Operation\s*:\s*([A-Z])', answer_text)
                pt = __import__('re').search(r'Problematic Team\s*:\s*([A-Z])', answer_text)
                if io:
                    parsed["illegal_operation"] = io.group(1).upper()
                if pt:
                    parsed["problematic_team"] = pt.group(1).upper()
    return parsed

# ==== Main ====

def run_nba_rulearena_benchmark():
    # Chargement clé et textes
    api_key = load_api_key(API_KEY_FILE)
    client = OpenAI(api_key=api_key)

    with open(RULES_FILE, "r", encoding="utf-8") as f:
        rules_text = f.read().strip()

    # Ici tu dois définir les opérations NBA (A, B, C...) et les situations des équipes.
    # Exemple minimal ; adapte / remplace par les vrais scénarios que tu veux benchmarker.
    operations_block = """Operation A: Team A trades Player X to Team B and receives Player Y. The combined salaries would put Team A over the salary cap without an exception.
Operation B: Team C signs a qualifying veteran free agent within the allowed window."""
    team_situations_block = """Team A: current salary $135,000,000, no exceptions used.
Team B: current salary $120,000,000, no exceptions used.
Team C: current salary $138,000,000, eligible for qualifying veteran exception."""

    # Construire la description utilisateur à passer à extract_facts_from_prompt
    user_description = build_nba_description(operations_block, team_situations_block)

    # Extraire les faits à partir des règles et de la description
    facts = extract_facts_from_prompt(rules_text, user_description, api_key)
    # Écrire facts dans facts.txt pour compatibilité downstream
    with open(FACTS_FILE, "w", encoding="utf-8") as f:
        f.write(facts.strip() + "\n")

    # Extraire entités, puis conclusions (remplit queries.txt)
    entities = extract_entities_from_file(FACTS_FILE)
    extract_conclusions(RULES_FILE, QUERIES_FILE, entities)

    # Construire la base de connaissances symbolique
    kb = pl.KnowledgeBase("nba_rulearena")
    facts_lines = read_file_strip_comments(FACTS_FILE)
    rules_lines = read_file_strip_comments(RULES_FILE)
    kb(facts_lines + rules_lines)

    # Lire les requêtes logiques
    queries = read_file_strip_comments(QUERIES_FILE)

    # Évaluer via pytholog
    results = []
    for q in queries:
        result = kb.query(pl.Expr(q))
        hit_in_facts = q in facts  # si la requête est littéralement dans le texte des faits
        passed = (result == ['Yes']) or hit_in_facts
        if passed:
            results.append(f"{q} -> {result}")
        else:
            results.append(f"{q} -> {result}")

    # Construire prompt d'explication final (optionnel, ici pour chaque opération on peut demander une explication)
    def build_explanation_prompt(user_description, rules, facts_text, results_list):
        return f"""
You are a symbolic reasoning assistant that explains conclusions drawn from logical reasoning.

User's input:
\"\"\"{user_description.strip()}\"\"\"

Rules:
\"\"\"{rules.strip()}\"\"\"

Facts extracted:
\"\"\"{facts_text.strip()}\"\"\"

Symbolic reasoning results:
{results_list}

Instructions:
1. Determine if any of the described operations violate the rules.
2. Justify using the extracted facts and applied rules.
3. Output in the format required:
   * "Answer : False." if no violation.
   * "Answer : True. Illegal Operation : X. Problematic Team : Y." if there is a violating operation.
4. Mention any applicable salary cap exceptions that explain compliance or violation.
"""

    # Préparer prompt d'explication
    facts_text = "\n".join(facts_lines)
    results_log = "\n".join(results)
    explanation_prompt = build_explanation_prompt(user_description, rules_text, facts_text, results_log)

    # Appel à l'API pour obtenir la décision finale
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": NBA_SYSTEM_PROMPT},
                  {"role": "user", "content": NBA_USER_PROMPT_BASE.replace("< reference_rules >", rules_text).replace("< user_query >", operations_block + "\nTeam Situations:\n" + team_situations_block)}],
        temperature=TEMPERATURE
    )
    llm_answer = response.choices[0].message.content.strip()

    # Analyse symbolique pour chaque query déjà faite
    print("Résultats symboliques :")
    for line in results:
        print(line)
    print("\nRéponse LLM finale :")
    print(llm_answer)

    # Synthèse simple
    summary = {
        "operations_block": operations_block,
        "team_situations_block": team_situations_block,
        "symbolic_results": results,
        "llm_answer": llm_answer
    }

    # Sauvegarde résumé
    with open("nba_rulearena_benchmark_summary.json", "w", encoding="utf-8") as f:
        import json
        json.dump(summary, f, indent=2)

    print("\nRésumé écrit dans nba_rulearena_benchmark_summary.json")


if __name__ == "__main__":
    run_nba_rulearena_benchmark()
