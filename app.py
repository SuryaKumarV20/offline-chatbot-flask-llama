from flask import Flask, request, jsonify, render_template
from llama_cpp import Llama
import uuid
from flask_cors import CORS
from memory import load_memory, save_memory, get_relevant_context
import glob, os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ✅ Updated function to find model relative to this script's location
def find_gguf_model(model_dir_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Current script dir
    model_dir = os.path.join(base_dir, model_dir_name)     # Absolute path to models/
    gguf_files = glob.glob(os.path.join(model_dir, "*.gguf"))
    if not gguf_files:
        raise FileNotFoundError("❌ No .gguf model found in 'models/' folder.")
    return gguf_files[0]

# ✅ Load model path reliably
model_path = find_gguf_model("models")

# ✅ Initialize model
llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=0  # CPU only
)

SYSTEM_PROMPT = "You are a concise assistant. Always answer clearly and directly."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        session_id = data.get("session_id", str(uuid.uuid4()))
        chat_id = str(data.get("chat_id", "default"))

        if not user_input:
            return jsonify({"response": "⚠️ Empty message.", "session_id": session_id, "chat_id": chat_id})

        memory_context = get_relevant_context(session_id, chat_id, user_input)
        history = [f"User: {m['user']}\nAssistant: {m['assistant']}" for m in memory_context]
        memory_prompt = "\n".join(history)

        full_prompt = f"System: {SYSTEM_PROMPT}\n{memory_prompt}\nUser: {user_input}\nAssistant:"

        output = llm(full_prompt, max_tokens=200, stop=["User:", "Assistant:"])
        text = output["choices"][0]["text"].strip()

        memory = load_memory(session_id, chat_id)
        memory.append({"user": user_input, "assistant": text})
        save_memory(session_id, chat_id, memory)

        return jsonify({"response": text, "session_id": session_id, "chat_id": chat_id})

    except Exception as e:
        return jsonify({"response": f"❌ Model error: {str(e)}", "session_id": "unknown", "chat_id": "default"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
#python bitsegments_localminds/app.py
