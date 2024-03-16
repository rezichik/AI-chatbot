from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyBTkTDOHr7gE7qUIOwPsOLwNJMPli-3bIg"

genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {"temperature": 0.9, "max_output_tokens": 2048}

model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
chat = model.start_chat(history=[])
history = ["", ""]

app = Flask(__name__)
app.secret_key = "melon"

def chat_bot(question):
    length = len(history)
    response = chat.send_message([history[length-2] + history[length-1] + question])

    history.append("my previous question: " + question + "\n")

    summery = (chat.send_message(["summarize this text shortly maximum 2 sentences: " + response.text])).text
    history.append("your previous answer on that question: " + summery + "\n")

    return response.text


@app.route('/')
def home():
    return render_template('index.html')

# Route to handle user input and provide response
@app.route('/get', methods=['GET'])
def get_bot_response():
    user_question = request.args.get('msg')
    return jsonify(chat_bot(user_question))

if __name__ == '__main__':
    app.run(debug=True)
