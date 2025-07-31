from extract_facts import *
from extract_rules import *
from extract_queries import *

import pytholog as pl
def load_api_key(filepath):
    with open(filepath, 'r') as f:
        return f.read().strip()

# Chargement de la clé API depuis le fichier
api_key = load_api_key("api_key.txt")



model="gpt-4"

# Création d'une base de connaissances

pdf_path = "advanced_orthopaedics_&_spor.pdf"
# pdf_path= "Hanoi.pdf"
# pdf_path = "Respiratory_Illness_Diagnostic_Guide.pdf"
# pdf_path="cgv-fr-fr-12-13.pdf"


    
rules = extract_rules_from_pdf(pdf_path, api_key)
rules_path = "rules.txt"
with open(rules_path, "r") as f:
    rules = f.read().strip()
user_description = """
Hi, I just wanted to check how much time off I can take this year. I’ve been working full-time  since 1 year and a half, and I'm based in the U.S. I haven’t taken any vacation or sick days yet this year, and I don’t have any leftover sick time from last year.

Could you let me know how many days off I’m entitled to in total this year, I want the answer in days?
"""

# user_description = """System Prompt - Tower of Hanoi
# You are a helpful assistant. Solve this puzzle for me.
# There are three pegs and 4 disks of different sizes stacked on the first peg. The disks are
# numbered from 1 (smallest) to 4 (largest). Disk moves in this puzzle should follow:
# 1. Only one disk can be moved at a time.
# 2. Each move consists of taking the upper disk from one stack and placing it on top of
# another stack.
# 3. A larger disk may not be placed on top of a smaller disk.
# The goal is to move the entire stack to the third peg.
# Example: With 3 disks numbered 1 (smallest), 2, and 3 (largest), the initial state is [[3, 2, 1],
# [], []], and a solution might be:
# moves = [[1 , 0 , 2] , [2 , 0 , 1] , [1 , 2 , 1] , [3 , 0 , 2] ,
# [1 , 1 , 0] , [2 , 1 , 2] , [1 , 0 , 2]]
# This means: Move disk 1 from peg 0 to peg 2, then move disk 2 from peg 0 to peg 1, and so on.
# Requirements:
# • When exploring potential solutions in your thinking process, always include the corresponding complete list of moves.
# • The positions are 0-indexed (the leftmost peg is 0).
# • Ensure your final answer includes the complete list of moves in the format:
# moves = [[disk id, from peg, to peg], ...]

# """
# user_description = """
# I am 15 years old. I've been experiencing persistent coughing and wheezing for more than a week now, accompanied by a fever above 38°C.
# I also have a sore throat, fatigue, and nasal congestion. Recently, I've been feeling short of breath
# and experiencing chest pain when I breathe. I've also noticed some confusion and dizziness. I have a history
# of allergies and asthma, but I'm not sure if these symptoms are related to that.
# """
# user_description = """
# Bonjour, j’ai pris un TGV InOui de Paris à Lyon avec un changement à Dijon. Tout était réservé en une seule fois via SNCF Connect.
# Mon TER entre Dijon et Lyon a eu 1h30 de retard, donc je suis arrivé en retard à Lyon.
# Est-ce que j’ai droit à un remboursement ou une compensation ?
# """



facts=extract_facts_from_prompt(rules,user_description, api_key) #Construct the facts from the user description and rules
facts_path = "facts.txt"



entities = extract_entities_from_file(facts_path)
extract_conclusions("rules.txt", "queries.txt", entities)





kb = pl.KnowledgeBase("medical")

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('%')]
    

file = load_lines("queries.txt")

kb(load_lines("facts.txt")+load_lines("rules.txt"))

results=[]
for query in file:
    # print(query)
    # Exécute la requête et affiche le résultat
    result = kb.query(pl.Expr(query))

    # print(f"Query: {query} -> Result: {result}")
    print(query in facts)
    if result==['Yes'] or query in facts:
        results.append(f"{query} -> {result}")
        print(f"Query: {query} -> Result: {result}")



def build_explanation_prompt(user_description, rules, facts, results, document_text=None):
    doc_section = f"\nDocument excerpt:\n\"\"\"{document_text.strip()}\"\"\"\n" if document_text else ""
    return f"""
You are a symbolic reasoning assistant that explains conclusions drawn from logical reasoning.

User's input (description and questions):
\"\"\"{user_description.strip()}\"\"\"

Rules used by the reasoning engine:
\"\"\"{rules.strip()}\"\"\"

Facts extracted:
\"\"\"{facts.strip()}\"\"\"

Results from symbolic reasoning:
{results}

{doc_section[:6000]}

Your task is to write a clear and accurate explanation in natural language. Follow these steps:
1. Directly answer any question(s) the user asked in their input.
2. Use the reasoning results to justify your answer with natural language.
3. When applicable, you may perform simple and transparent conversions (e.g., hours to days using 8 hours = 1 day) to help the user understand the outcome.
4. Always justify your answer using:
   - The facts that were extracted from the user input
   - The rules that were applied to reach the conclusion
5. Do not make assumptions not supported by the facts or rules.

Base your explanation only on what was logically inferred, and what can be derived using basic arithmetic from it.

Now write your explanation, clearly and concisely, in no more than 200 words:
"""


# Chargement des faits et résultats
with open("facts.txt") as f:
    facts_text = f.read()
    
results_log = ""
for query in file:
    result = kb.query(pl.Expr(query))
    results_log += f"{query} -> {result}\n"

# Construction du prompt
document_text = extract_text_from_pdf(pdf_path) #Extract the pdf for the final prompt

final_prompt = build_explanation_prompt(user_description, rules, facts_text, results_log,document_text)

# Appel à l’API OpenAI pour générer la réponse en langage naturel
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0.2
    )




print("\n Final Answer in Natural Language:\n")
print(response.choices[0].message.content)