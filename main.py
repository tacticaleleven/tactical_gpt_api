from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🚀 Tactical Eleven GPT API is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    # Zorunlu alanları kontrol et
    required_fields = ["prompt", "user_type", "model"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is missing"}), 400

    prompt = data["prompt"]
    user_type = data["user_type"]
    requested_model = data["model"]

    # user_type = trial ise GPT-4 isteğini engelle
    if user_type == "trial" and requested_model == "gpt-4":
        model_used = "gpt-3.5-turbo"
    else:
        model_used = requested_model

    try:
        response = openai.ChatCompletion.create(
            model=model_used,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return jsonify({
            "response": response.choices[0].message["content"],
            "model_used": model_used
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
