from flask import Flask, request, jsonify
from main import search_and_respond
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables
env_path = pathlib.Path(__file__).parent.absolute() / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the message from the request
        data = request.get_json()
        
        # Extract the message from WhatsApp webhook format
        # Note: You'll need to adjust this based on your specific WhatsApp Business API setup
        message = data.get('message', {}).get('text', '')
        
        if not message:
            return jsonify({'error': 'No message found in request'}), 400
            
        # Get the answer using our RAG system
        answer = search_and_respond(message)
        
        # Return the response in a format suitable for WhatsApp
        return jsonify({
            'message': answer
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True) 