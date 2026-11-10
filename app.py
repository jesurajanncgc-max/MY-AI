import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# உங்கள் Gemini API Key-ஐ இங்கு குறிப்பிடவும்
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LtTQKrvjo2fWblCvjoSqpeuaQPe6DJxYq6jc_vvWBbpQ")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    user_query = data.get("question", "")

    if not user_query:
        return jsonify({"error": "Please ask a question."}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=user_query,
            config={
                "system_instruction": (
                    "நீ மாணவர்களுக்கான ஒரு சிறந்த பாட ஆசிரியர். "
                    "கணிதம், அறிவியல், கணினி அறிவியல் மற்றும் பிற பாடங்களில் "
                    "மாணவர்கள் கேட்கும் சந்தேகங்களுக்கு மிகவும் எளிமையாகவும், "
                    "புரியும் படியும், படிப் படியாக தெளிவான விளக்கங்களை தமிழில் வழங்க வேண்டும்."
                )
            }
        )
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)