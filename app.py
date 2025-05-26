from flask import Flask, jsonify, request, render_template
import os
import socket

app = Flask(__name__)

# Dictionary to store RFID tag actions
RFID_ACTIONS = {
    # Add your RFID tag IDs and their corresponding actions here
    "TAG1": "action1",
    "TAG2": "action2",
    # Example: "123456789": "unlock_door"
}

def get_ip_address():
    try:
        # Get the IP address of the Raspberry Pi
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Could not determine IP address"

def execute_rfid_action(tag_id):
    """
    Execute the action associated with the RFID tag
    Add your custom actions here
    """
    if tag_id in RFID_ACTIONS:
        action = RFID_ACTIONS[tag_id]
        print(f"Executing action for tag {tag_id}: {action}")
        # Add your action execution logic here
        # For example:
        # if action == "unlock_door":
        #     unlock_door()
        return f"Executed action: {action}"
    else:
        print(f"Unknown RFID tag: {tag_id}")
        return "Unknown tag"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'ip_address': get_ip_address()
    })

@app.route('/api/message', methods=['GET', 'POST'])
def handle_message():
    if request.method == 'POST':
        data = request.get_json()
        
        # Handle RFID data
        if data.get('message') == 'rfid':
            rfid_data = data.get('rfid_data')
            if rfid_data:
                result = execute_rfid_action(rfid_data)
                return jsonify({
                    'status': 'success',
                    'message': 'RFID tag processed',
                    'tag_id': rfid_data,
                    'result': result
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'No RFID data provided'
                }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Received your message',
            'data': data
        })
    else:
        return jsonify({
            'status': 'success',
            'message': 'Send a POST request with your message',
            'example': {'message': 'rfid', 'rfid_data': 'TAG1'}
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    ip = get_ip_address()
    print(f"\nServer starting...")
    print(f"Local URL: http://localhost:{port}")
    print(f"Network URL: http://{ip}:{port}")
    print("Press CTRL+C to quit\n")
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production 