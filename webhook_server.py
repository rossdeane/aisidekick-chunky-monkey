from flask import Flask, request, jsonify
from main import search_and_respond
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables
env_path = pathlib.Path(__file__).parent.absolute() / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

app = Flask(__name__)

# WhatsApp webhook verification endpoint
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Get the verification token from the query parameters
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Get the verification token from environment variables
    verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
    
    # Check if the request is for verification
    if mode and token:
        # Check if the token matches
        if mode == 'subscribe' and token == verify_token:
            # Return the challenge
            return challenge, 200
        else:
            # Return an error if the token doesn't match
            return jsonify({'error': 'Invalid verification token'}), 403
    else:
        # Return an error if the parameters are missing
        return jsonify({'error': 'Missing verification parameters'}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the webhook data from the request
        data = request.get_json()
        
        # Check if this is a messages webhook
        if data.get('field') != 'messages':
            return jsonify({'error': 'Not a messages webhook'}), 400
            
        # Extract the value object which contains the message details
        value = data.get('value', {})
        
        # Extract the first message from the messages array
        messages = value.get('messages', [])
        if not messages:
            return jsonify({'error': 'No messages found in webhook'}), 400
            
        message = messages[0]
        
        # Check if this is a text message
        if message.get('type') != 'text':
            return jsonify({'error': 'Not a text message'}), 400
            
        # Extract the message text
        message_text = message.get('text', {}).get('body', '')
        
        if not message_text:
            return jsonify({'error': 'No message text found'}), 400
            
        # Get the answer using our RAG system
        answer = search_and_respond(message_text)
        
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