from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

# ⚠️ Ollama doit déjà tourner avec un modèle : ex. `ollama run phi`

# 1. Création de l'objet LLM
llm = ChatOllama(model="llama2")  # ou "llama2", "mistral", etc.

# 2. Construction du prompt
messages = [
    SystemMessage(content="You are a helpful assistant answer in less than 100 words."),
    HumanMessage(content="Can you provide the mathematical proof that the sum of two odd numbers always results in an odd number?")]

# 3. Appel du modèle
response = llm(messages)

# 4. Affichage de la réponse
print(response.content)