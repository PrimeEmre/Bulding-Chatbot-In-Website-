from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "emre_ai_secret_123"

@app.route("/")
def home():
    session["history"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    history = session.get("history", [])

    history.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": "deepseek-r1:8b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful and friendly AI assistant named Jarvis."
            }
        ] + history,
        "stream": False
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=120
        )

        result = response.json()
        ai_message = result["message"]["content"]

        history.append({
            "role": "assistant",
            "content": ai_message
        })

        session["history"] = history
        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)