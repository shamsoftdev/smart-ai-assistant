# repositories/memory_repository.py

chat_memory = {}

def get_history(user: str):
    return chat_memory.get(user, [])

def save_message(user: str, role: str, message: str):
    if user not in chat_memory:
        chat_memory[user] = []

    chat_memory[user].append({
        "role": role,
        "message": message
    })