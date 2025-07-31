import fitz  # PyMuPDF
from openai import OpenAI

# 1. Récupère le texte depuis un fichier PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def build_facts_prompt(user_description, rules):
    return f"""
You are a symbolic reasoning assistant that extracts logical facts from a case description.

Your goal is to extract **as many relevant and accurate facts as possible**, while ensuring they match the structure and vocabulary defined in the rules below:

{rules}

Each fact must follow this exact format (no period at the end):
predicate(entity, value)

Where:
- 'entity' is a lowercase constant (e.g., subject, user, person, item)
- 'predicate' must be chosen from those found in the rules (e.g., has, is, may_have, require, causes, etc.)
- 'value' must use the same terms or categories that appear in the rules. Do **not** invent new ones.

INSTRUCTIONS:
- Be thorough: extract **all relevant facts** that clearly appear or are directly implied by the description.
- Be consistent: reuse the **same predicates and value terms** as in the rules.
- Do **not** guess or invent values or predicates not found in the rules.
- Do **not** use uppercase letters for entities.
- Do **not** use any bullets, numbering, or extra explanations.
- Do not extract the conclusions from the rules document but the predicates.

NUMERIC VALUES:
If the description includes numerical values (e.g., "temperature of 39", "score less than 5"), and the rules use thresholds, then map the value accordingly using suffixes:
- `_gt_N` for "greater than N"
- `_lt_N` for "less than N"
- `_ge_N` for "greater or equal to N"
- `_le_N` for "less or equal to N"
Use only thresholds that appear in the rules.

✔ Correct examples:
has(user, fever_gt_38)  
has(subject, experience_lt_5)  
is(candidate, eligible)  
has(car, pressure_lt_90)  
is(machine, active)

Now extract all relevant logical facts from the following case description :

\"\"\"{user_description}\"\"\"
"""




# 3. Appeler OpenAI API
def extract_facts_from_prompt(rules, user_description, api_key, model="gpt-4"):
    prompt = build_facts_prompt(user_description,rules)

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    facts = response.choices[0].message.content
    with open("facts.txt","w") as f:
        f.write(facts)

    return response.choices[0].message.content

#  Exemple d’utilisation
if __name__ == "__main__":
    rules_path = "rules.txt"
    with open(rules_path, "r") as f:
        rules = f.read().strip()
    
    user_description = """
I've been experiencing persistent coughing for more than a week now, accompanied by a fever above 38°C.
I also have a sore throat, fatigue, and nasal congestion. Recently, I've been feeling short of breath
and experiencing chest pain when I breathe. I've also noticed some confusion and dizziness. I have a history
of allergies and asthma, but I'm not sure if these symptoms are related to that.
"""
    facts=extract_facts_from_prompt(rules,user_description, api_key)
    # print("\nExtracted Facts:\n")
    # print(facts)
