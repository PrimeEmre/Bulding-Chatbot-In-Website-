from flask import Flask, render_template, request, jsonify, session
import requests
import json

app = Flask(__name__)
app.secret_key = "emre_ai_secret_123"

# ─────────────────────────────────────────
# ROUTE: Main page
# ─────────────────────────────────────────
@app.route("/")
def home():
    # Clear conversation history when page loads
    session["history"] = []
    return render_template("index.html")

# ─────────────────────────────────────────
# ROUTE: Chat endpoint (called by the browser)
# ─────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    # Get the message the user typed
    user_message = request.json.get("message", "")

    # Load conversation history from session
    history = session.get("history", [])

    # Add user message to history
    history.append({
        "role": "user",
        "content": user_message
    })

    # Build the request to send to Ollama
    payload = {
        "model": "deepseek-r1:8b",  # change if you use a different model
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful and friendly AI assistant named Jarvis."
            }
        ] + history,
        "stream": False
    }

    try:
        # Send request to Ollama
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=120
        )

        # Extract AI response
        result = response.json()
        ai_message = result["message"]["content"]

        # Add AI response to history so it remembers the conversation
        history.append({
            "role": "assistant",
            "content": ai_message
        })

        # Save updated history to session
        session["history"] = history

        # Send response back to the browser
        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)