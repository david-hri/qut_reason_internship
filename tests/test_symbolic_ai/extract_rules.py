import fitz  # PyMuPDF
from openai import OpenAI

# 1. Récupère le texte depuis un fichier PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 2. Définir le prompt généraliste
def build_prompt(document_text):
    return f"""
You are a symbolic reasoning engine.

Your task is to read a descriptive document and extract logical rules that can be used for automated reasoning. The rules must follow a first-order logic or Datalog-style Horn clause syntax.

Each rule must follow **strictly** this format (without any period at the end):
head :- condition1, condition2, ..., conditionN

Where:
- `head` is the conclusion or result (e.g., eligible(X, refund))
- The conditions describe required facts using predicates (e.g., has(X, delay_gt_60), paid(X, single_payment), includes(X, sncf_connect))
- Use predicates like: has, is, may_have, require, triggers, includes, causes, eligible, located_in, owns, needs, etc.
- Always use `X` as the main entity (e.g., traveler, person, document)
- Do **not** use natural language or explanations
- Do **not** add periods at the end of rules

🔍 Pay special attention to the following:
1. Identify all **“if... then...”** patterns (even if implicit)
2. Identify all **numerical thresholds or conditions** (delays in minutes, percentages, payment amounts, duration of service, etc.) and convert them using suffixes like:
   - `_gt_N` for greater than N
   - `_lt_N` for less than N
   - `_ge_N` for greater or equal to N
   - `_le_N` for less or equal to N
   - `_eq_N` for equal to N (if applicable)
3. Encode all constants using lowercase and underscores only (e.g., more_than_one_hour → delay_gt_60)

✅ Correct examples:
eligible(X, refund) :- has(X, delay_gt_60), paid(X, single_payment), assembled_by(X, sncf_connect)
must_provide(X, assistance) :- has(X, delay_ge_120), includes(X, tgv_inoui), located_in(X, france)
eligible(X, re_routing) :- has(X, delay_ge_60), not(has(X, additional_costs)), includes(X, ter)

You must extract all applicable rules from the following document (first 6000 characters only). Do not add explanations or commentary.

Now extract the logical rules from this text:

{document_text[:6000]}
"""



# 3. Appeler OpenAI API
def extract_rules_from_pdf(pdf_path, api_key):
    document_text = extract_text_from_pdf(pdf_path)
    prompt = build_prompt(document_text)

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    with open("rules.txt", "w") as f:
        rules = response.choices[0].message.content
    # Nettoyage des règles : suppression des points finaux et des espaces inutiles
        cleaned_rules = [line.rstrip('.').strip() for line in rules.split('\n') if line.strip()]
    
    # Écriture des règles nettoyées dans le fichier
        f.write('\n'.join(cleaned_rules))

    return '\n'.join(cleaned_rules)


# 🔁 Exemple d’utilisation
if __name__ == "__main__":
    pdf_path = "Respiratory_Illness_Diagnostic_Guide.pdf"
    

    
    rules = extract_rules_from_pdf(pdf_path, api_key)
    print("\nExtracted Rules:\n")
    print(rules)
