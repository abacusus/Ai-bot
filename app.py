from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
app = Flask(__name__)
print("✅ Flask app initialized")  # Debug print

# Enable CORS
CORS(app)
print("✅ CORS enabled")  # Debug print

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["15 per minute"]
)
print("✅ Rate limiter configured")  # Debug print

# Load environment variables
load_dotenv()
print("✅ Environment variables loaded")  # Debug print

# Configure OpenAI
openai.api_key = os.getenv("API_KEY")
print(f"🔑 API Key loaded: {'*****' + openai.api_key[-4:] if openai.api_key else 'NOT FOUND'}")  # Debug print (shows last 4 chars)

if not openai.api_key:
    raise RuntimeError("❌ OPENAI_API_KEY environment variable not set!")

@app.route('/')
def home():
    print("🔄 Home route accessed")  # Debug print
    try:
        # Debug template loading
        template_path = os.path.join(app.root_path, 'templates', 'index.html')
        print(f"📄 Looking for template at: {template_path}")
        if not os.path.exists(template_path):
            print("❌ Template not found at the expected location")
        
        return render_template('index.html')
    except Exception as e:
        print(f"❌ Error in home route: {str(e)}")  # Debug print
        raise

@app.route('/chat', methods=['POST'])
@limiter.limit("5 per minute")
def chat():
    print("🔄 /chat endpoint hit")  # Debug print
    try:
        data = request.get_json()
        print(f"📩 Received data: {data}")  # Debug print
        
        user_message = data.get('message', '').strip()
        print(f"💬 Message received: '{user_message}'")  # Debug print
        
        if not user_message:
            print("⚠️ Empty message received")  # Debug print
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        print("🤖 Calling OpenAI API...")  # Debug print
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=250
        )
        print("✅ OpenAI API call successful")  # Debug print
        
        reply = response.choices[0].message.content.strip()
        print(f"📤 Sending reply: {reply[:50]}...")  # Debug print (first 50 chars)
        
        return jsonify({'reply': reply})
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    print(f"🚀 Starting Flask server (debug={debug_mode})")  # Debug print
    app.run(debug=debug_mode)
