import pytholog as pl

# Création d'une base de connaissances
kb = pl.KnowledgeBase("medical")

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('%')]
    

file = load_lines("queries.txt")

kb(load_lines("facts.txt")+load_lines("rules.txt"))


for query in file:
    # Exécute la requête et affiche le résultat
    result = kb.query(pl.Expr(query))
    print(f"Query: {query} -> Result: {result}")