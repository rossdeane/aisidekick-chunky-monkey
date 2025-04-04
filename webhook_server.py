from flask import Flask, request, jsonify
from main import search_and_respond
import os
from dotenv import load_dotenv
import pathlib
import json
import logging
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('webhook.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = pathlib.Path(__file__).parent.absolute() / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

# WhatsApp API credentials
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN')

# WhatsApp API endpoint
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

app = Flask(__name__)

# Function to send a WhatsApp message
def send_whatsapp_message(to, message):
    """
    Send a WhatsApp message using the WhatsApp Cloud API.
    
    Args:
        to (str): The recipient's phone number
        message (str): The message to send
        
    Returns:
        dict: The API response
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to {to}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {str(e)}")
        return {"error": str(e)}

# WhatsApp webhook verification endpoint
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Get the verification token from the query parameters
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Check if the request is for verification
    if mode and token:
        # Check if the token matches
        if mode == 'subscribe' and token == WHATSAPP_VERIFY_TOKEN:
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
        
        # Log the entire webhook payload for debugging
        logger.info(f"Received webhook data: {json.dumps(data, indent=2)}")
        
        # Check if this is a WhatsApp Business Account webhook
        if data.get('object') != 'whatsapp_business_account':
            logger.warning(f"Not a WhatsApp Business Account webhook: {data.get('object')}")
            return jsonify({'error': 'Not a WhatsApp Business Account webhook'}), 400
            
        # Extract the entry array
        entries = data.get('entry', [])
        if not entries:
            logger.warning("No entries found in webhook")
            return jsonify({'error': 'No entries found in webhook'}), 400
            
        # Process all entries
        responses = []
        for entry in entries:
            logger.info(f"Processing entry: {json.dumps(entry, indent=2)}")
            
            # Extract the changes array
            changes = entry.get('changes', [])
            if not changes:
                logger.warning("No changes found in entry")
                continue
                
            # Process all changes
            for change in changes:
                logger.info(f"Processing change: {json.dumps(change, indent=2)}")
                
                # Check if this is a messages webhook
                if change.get('field') != 'messages':
                    logger.warning(f"Not a messages webhook: {change.get('field')}")
                    continue
                    
                # Extract the value object which contains the message details
                value = change.get('value', {})
                logger.info(f"Webhook value: {json.dumps(value, indent=2)}")
                
                # Extract all messages from the messages array
                messages = value.get('messages', [])
                if not messages:
                    logger.warning("No messages found in webhook")
                    continue
                    
                # Process all messages
                for message in messages:
                    logger.info(f"Processing message: {json.dumps(message, indent=2)}")
                    
                    # Check if this is a text message
                    if message.get('type') != 'text':
                        logger.warning(f"Not a text message: {message.get('type')}")
                        continue
                        
                    # Extract the message text
                    message_text = message.get('text', {}).get('body', '')
                    
                    if not message_text:
                        logger.warning("No message text found")
                        continue
                        
                    logger.info(f"Extracted message text: {message_text}")
                    
                    # Get the answer using our RAG system
                    answer = search_and_respond(message_text)
                    logger.info(f"Generated answer: {answer}")
                    
                    # Get the sender's phone number
                    sender_phone = message.get('from')
                    
                    # Send the response back to the sender
                    if sender_phone:
                        send_result = send_whatsapp_message(sender_phone, answer)
                        logger.info(f"Send result: {json.dumps(send_result, indent=2)}")
                        
                        # Add the response to our list
                        responses.append({
                            'message': answer,
                            'to': sender_phone,
                            'send_result': send_result
                        })
        
        # If we processed any messages, return the responses
        if responses:
            return jsonify(responses)
        else:
            return jsonify({'error': 'No valid messages to process'}), 400
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5001))
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True) 