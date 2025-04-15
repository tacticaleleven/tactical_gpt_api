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

    response_format = data.get("response_format")

    if response_format == "structured_tactical_json":
        messages.append({
            "role": "system",
            "content": (
                "Sen bir futbol menajerlik taktik analiz uzmanısın. "
                "Kullanıcıdan gelen verilerle yalnızca aşağıdaki JSON formatında yanıt ver:\n"
                "{\n"
                "  \"match_plan\": {\"attack\": {...}, \"defense\": {...}},\n"
                "  \"second_half_plan\": {\"if_winning\": {...}, \"if_losing\": {...}},\n"
                "  \"general_strategy\": {\"attack\": {...}, \"defense\": {...}},\n"
                "  \"losing_plan\": {...}\n"
                "}\n"
                "Her value kısa ve net, her reason detaylı açıklayıcı olsun. "
                "Sadece JSON olarak yanıt döndür. Açıklama, markdown veya metin E K L E M E.\n"
                "📌 Dikkat: 'general_strategy' alanı, 'match_plan' ile çelişmemelidir. "
                "Genel strateji, maç başı taktiğini desteklemeli ve tutarlı olmalıdır."
            )
        })

    elif response_format == "structured_with_how":
        messages.append({
            "role": "system",
            "content": (
                "Sen bir futbol menajerlik oyununda taktik önerileri yapan bir yapay zekasın. "
                "Kullanıcıdan gelen maç analiz verilerine göre aşağıdaki JSON formatında yanıt ver:\n"
                "{\n"
                "  \"match_plan\": {\"attack\": {...}, \"defense\": {...}},\n"
                "  \"second_half_plan\": {\"if_winning\": {...}, \"if_losing\": {...}},\n"
                "  \"general_strategy\": {\"attack\": {...}, \"defense\": {...}},\n"
                "  \"losing_plan\": {...}\n"
                "}\n\n"
                "Her alan şunları içermelidir:\n"
                "- focus: Ne yapılmalı? (kısa ve net)\n"
                "- reason: Neden yapılmalı? (1–2 cümle açıklayıcı)\n"
                "- how: Oyundaki 'Taktikler' menüsünde hangi ayarlar yapılmalı?\n\n"
                "🎮 how alanında SADECE aşağıdaki seçenekleri kullan:\n\n"
                "1. ATAK:\n"
                "- Takım Anlayışı: Sert Savunma, Savunma, Normal, Hücum, Sert Hücum\n"
                "- Pas Yönü: Karışık, Her iki kanattan, Sağ Kanattan, Sol Kanattan, Ortadan\n"
                "- Pas Atma Şekli: Kısa, Karışık, Uzun\n"
                "- Kontra Atağa Zorla: Açık, Kapalı\n\n"
                "2. SAVUNMA:\n"
                "- Pres Tarzı: Alçak, Yüksek\n"
                "- Top Çalma Tarzı: Kolay, Normal, Zor\n"
                "- Markaj Tarzı: Bölgesel, Adam Adama\n"
                "- Ofsayt Taktiği Uygula: Açık, Kapalı\n\n"
                "📌 'general_strategy' mutlaka 'match_plan' ile uyumlu olmalıdır. "
                "Çelişen ayar veya taktik kullanma.\n"
                "🛑 Bu kelimelerin dışında ifade veya yorum kullanma. "
                "Yanıt sadece JSON olsun. Açıklama, markdown veya yorum ekleme."
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

        try:
            parsed_output = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed_output = raw_output

        return jsonify({
            "model_used": model_used,
            "response": parsed_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
