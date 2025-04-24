from flask import Flask, request, jsonify
from ocr_cleaner_strict import clean_ocr_lines_strict  # Temizleyici modül

app = Flask(__name__)

@app.route('/clean', methods=['POST'])
def clean_ocr():
    data = request.get_json()
    lines = data.get("lines", [])

    if not isinstance(lines, list):
        return jsonify({"error": "lines must be a list of strings"}), 400

    cleaned_lines = clean_ocr_lines_strict(lines)
    return jsonify({"cleaned_lines": cleaned_lines})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
