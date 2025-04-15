from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "🚀 Tactical Eleven GPT API is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    # Zorunlu alanlar kontrolü
    required_fields = ["prompt", "user_type", "model"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is missing"}), 400

    prompt = data["prompt"]
    user_type = data["user_type"]
    requested_model = data["model"]

    # Trial kullanıcı GPT-4 isterse downgrade
    model_used = "gpt-3.5-turbo" if user_type == "trial" and requested_model == "gpt-4" else requested_model

    # Mesajlar dizisi hazırlanıyor
    messages = []

    # Eğer structured format istendiyse system mesajı ekleniyor
    if data.get("response_format") == "structured_tactical_json":
        messages.append({
            "role": "system",
            "content": (
                "Sen bir futbol menajerlik taktik analiz uzmanısın. "
                "Kullanıcıdan gelen verilerle yalnızca aşağıdaki JSON formatında yanıt ver:\n"
                "{\n"
                "  \"match_plan\": {\"attack\": {...}, \"defense\": {...}},\n"
                "  \"losing_plan\": {...},\n"
                "  \"attacking_strategy\": {...},\n"
                "  \"defensive_strategy\": {...},\n"
                "  \"second_half_plan\": {...}\n"
                "}\n"
                "Her value kısa ve net, her reason detaylı açıklayıcı olsun. "
                "Sadece JSON olarak yanıt döndür. Açıklama, markdown veya metin E K L E M E."
            )
        })

    # Kullanıcı mesajı
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model_used,
            messages=messages,
            temperature=0.7
        )

        raw_output = response.choices[0].message["content"]

        # JSON string dönmüşse parse etmeye çalış
        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_output = raw_output  # string olarak bırak

        return jsonify({
            "model_used": model_used,
            "response": parsed_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
