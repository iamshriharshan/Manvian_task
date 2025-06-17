from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

API_KEY = "Enter_API_Key"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
system_prompt = (
    "You are a strict technical interviewer for software engineering roles. "
    "start the interview slowely , interact first and then start"
    "give qustion starting from this Question:1" 
    "You will ask one question at a time. After the user responds, give a short evaluation "
    "and ask the next relevant question. Cover topics like data structures, algorithms, system design, "
    "and coding logic. Keep it professional and focused."
)
chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_with_bot():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
