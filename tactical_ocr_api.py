from flask import Flask, request, jsonify
from ocr_cleaner_strict import clean_ocr_lines_strict

import os

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
