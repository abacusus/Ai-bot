from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace this with your actual API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )

    reply = response['choices'][0]['message']['content'].strip()
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
