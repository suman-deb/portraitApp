#/backend/app.py
# This is a simple Flask application that uses OpenAI's API 
# to generate a list of works by a given person.
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app) # ← enable CORS for frontend access

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    person_name = data.get("name", "")

    if not person_name:
        return jsonify({"error": "Missing person name"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"List 5 popular poems, songs, or quotes by {person_name}."}
            ],
            temperature=0.7,
            max_tokens=200,
        )

        works_text = response.choices[0].message.content.strip()
        return jsonify({"works": works_text})

    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
