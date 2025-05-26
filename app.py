from flask import Flask, jsonify, request
import os
import socket

app = Flask(__name__)

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

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Server is running',
        'ip_address': get_ip_address(),
        'port': int(os.environ.get('PORT', 5000))
    })

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
        return jsonify({
            'status': 'success',
            'message': 'Received your message',
            'data': data
        })
    else:
        return jsonify({
            'status': 'success',
            'message': 'Send a POST request with your message'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    ip = get_ip_address()
    print(f"\nServer starting...")
    print(f"Local URL: http://localhost:{port}")
    print(f"Network URL: http://{ip}:{port}")
    print("Press CTRL+C to quit\n")
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production 