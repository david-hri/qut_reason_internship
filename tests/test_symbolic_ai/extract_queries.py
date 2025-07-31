import re

def extract_entities_from_file(file_path):
    entities = set()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('%'):
                match = re.match(r"\w+\(([^,]+),", line)
                if match:
                    entities.add(match.group(1))
    return entities

# Exemple d'utilisation



def extract_conclusions(input_file, output_file, entities):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if ':-' in line:
                conclusion = line.split(':-')[0].strip()
                
                # Trouver toutes les variables majuscules (comme X, Y)
                variables = re.findall(r'\b([A-Z]\w*)\b', conclusion)
                
                if not variables:
                    outfile.write(conclusion + '\n')
                else:
                    for entity in entities:
                        new_conclusion = conclusion
                        for var in variables:
                            new_conclusion = new_conclusion.replace(var, entity)
                        outfile.write(new_conclusion + '\n')

if __name__ == "__main__":
    file_path = "facts.txt"
    entities = extract_entities_from_file(file_path)
    print("Entités extraites :", entities)
    print(entities, "entities")
    input_file = "rules.txt"  # Fichier contenant les règles
    output_file = "queries.txt"  # Fichier où écrire les conclusions
    extract_conclusions("rules.txt", "queries.txt", entities)
    print(f"Conclusions extraites et écrites dans {output_file}")