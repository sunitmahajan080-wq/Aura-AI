import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__, template_folder=".")

client = genai.Client()

SYSTEM_PROMPT = (
    "You are Aura AI, a helpful, intelligent, and aesthetic AI assistant. "
    "Always identify yourself as Aura AI. "
    "Respond naturally in the EXACT same language that the user writes to you in."
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": SYSTEM_PROMPT,
        "temperature": 0.7
    }
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'reply': ''})
    
    response = chat.send_message(user_message)
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
