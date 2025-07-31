from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('X, score, X_score, eligible, in_context, inherits, active_in, C1, C2, Rule')

# 1. Faits
+score('john', 15)
+in_context('john', 'france')
+inherits('france', 'europe')

# 2. Règle : une personne est eligible si son score est > 10
eligible(X) <= (score(X, X_score)) & (X_score > 10)

# 3. Règle : contexte actif
# Une règle active dans un contexte C2 est aussi active dans C1 si C1 hérite de C2
active_in(C1, Rule) <= inherits(C1, C2) & active_in(C2, Rule)

# 4. On peut dire qu'une règle est active dans le contexte 'europe'
+active_in('europe', 'eligible(X) <= score(X, X_score) & (X_score > 10)')

# ---------------------
# ✅ Interrogations
# ---------------------

print("Qui est éligible ?")
print(eligible(X))

print("\nLa règle d'éligibilité est-elle active en France ?")
print(active_in('france', X))
