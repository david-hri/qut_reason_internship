from openai import OpenAI
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def load_api_key(filepath):
    with open(filepath, 'r') as f:
        return f.read().strip()

# Chargement de la clé API depuis le fichier
api_key = load_api_key("api_key.txt")

client = OpenAI(api_key=api_key)

# Étape 1: Générer des embeddings pour tes documents
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"  # ou "text-embedding-3-large"
    )
    return np.array(response.data[0].embedding)

# Exemple : tes documents
documents = [
    "Le congé payé est de 25 jours par an en France.",
    "Les employés doivent poser leur demande de congé 3 jours à l’avance.",
    "Les chiens ne font pas des chats"
]

original_prompt=get_embedding("Hi, I just wanted to check how much time off I can take this year. I’ve been working full-time  since 1 year and a half, and I'm based in the U.S. I haven’t taken any vacation or sick days yet this year, and I don’t have any leftover sick time from last year. Could you let me know how many days off I’m entitled to in total this year, I want the answer in days?")
# Génération des embeddings
doc_embeddings = [get_embedding(doc) for doc in documents]

for i in doc_embeddings:
        print(np.dot(i, original_prompt))
print("Embeddings générés pour les documents.", doc_embeddings)

def search_similar_docs(query, documents, doc_embeddings, top_k=2):
    query_embedding = get_embedding(query)
    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [documents[i] for i in top_indices]

