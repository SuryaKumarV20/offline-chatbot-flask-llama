import os
import json

def load_memory(session_id, chat_id):
    path = f"memory/{session_id}_{chat_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_memory(session_id, chat_id, memory):
    os.makedirs("memory", exist_ok=True)
    path = f"memory/{session_id}_{chat_id}.json"
    with open(path, "w") as f:
        json.dump(memory, f)

def get_relevant_context(session_id, chat_id, user_input):
    return load_memory(session_id, chat_id)[-5:]  # last 5 messages only
