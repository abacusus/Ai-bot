from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS if frontend is separate

# Rate limiting (15 requests/minute)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["15 per minute"]
)

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
@limiter.limit("5 per minute")  # Stricter limit for chat endpoint
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=250
        )
        
        return jsonify({
            'reply': response.choices[0].message.content.strip()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
