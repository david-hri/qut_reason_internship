from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import openai

def get_chatgpt_move(history):
    """Envoie l'historique des coups à ChatOllama et récupère le prochain coup suggéré."""
    llm = ChatOllama(model="gpt-3", temperature=0)
    prompt = f"Nous jouons aux échecs. Voici l'historique des coups : {history}\nQuel est ton prochain coup ? Réponds uniquement avec un coup en notation standard (ex: e4, Nf3, dxe5)."
    
    messages = [{"role": "system", "content": "Tu es un joueur d'échecs qui répond uniquement avec des coups valides en notation standard."},
                {"role": "user", "content": prompt}]
    
    messages = [
            SystemMessage(content=f"Tu es un joueur d'échecs qui répond uniquement avec des coups valides en notation standard. Tu ne dois renvoyé que le coup et pas les explications"),
            HumanMessage(content=prompt)
        ]
    
    response=llm(messages).content.strip()
    return response

def main():
    history = ""
    print("Début de la partie !")
    
    while True:
        move = input("Votre coup (notation standard, ex: e4, Nf3) : ")
        history += f"Humain : {move}\n"
        
        print("ChatGPT réfléchit...")
        ai_move = get_chatgpt_move(history)
        print(f"ChatGPT joue : {ai_move}")
        history += f"ChatGPT : {ai_move}\n"
    
if __name__ == "__main__":
    main()