
from openai import OpenAI

def load_api_key(filepath):
    with open(filepath, 'r') as f:
        return f.read().strip()



api_key =load_api_key("api_key.txt")
from openai import OpenAI

def build_system_prompt():
    return """
You are a helpful assistant. 
"""

def build_user_prompt(n_disks: int):
    return f"""
Peux-tu me faire la démonstrationmathématique que la somme de deux
nombres impairs donnera toujours un nombre impair ?"""

def ask_gpt4_tower_of_hanoi(n_disks=5):
    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": build_user_prompt(n_disks)},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ou "gpt-4" si tu as accès
        messages=messages,
        temperature=0.0,
        max_tokens=2000,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    answer = ask_gpt4_tower_of_hanoi(15)
    print(answer)
