# server.py

import socket
import json
import uuid  
from blockchain import Blockchain

users = {
    "doctor": {"password": "doc123", "role": "doctor"},
    "diagnostic": {"password": "diag123", "role": "diagnostic"},
    "pharmacy": {"password": "pharma123", "role": "pharmacy"}
}

sessions = {}  

def authenticate(username, password):
    return username in users and users[username]["password"] == password

def handle_client(client_socket, blockchain):
    try:
        authenticated_user = None
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            request = json.loads(data)
            if request['action'] == 'login':
                username = request['username']
                password = request['password']
                if authenticate(username, password):
                    authenticated_user = username
                    session_token = str(uuid.uuid4())  
                    sessions[session_token] = username  
                    response = {'message': 'Login successful', 'role': users[username]['role'], 'session_token': session_token}
                else:
                    response = {'message': 'Invalid credentials'}
                client_socket.send(json.dumps(response).encode('utf-8'))

            elif request.get('session_token') in sessions:
                authenticated_user = sessions[request['session_token']]
                if request['action'] == 'add_block':
                    block_header = request['block_header']
                    block_data = request['block_data']
                    blockchain.new_block(block_header, block_data)
                    response = {
                        'message': 'Block added successfully!',
                        'block': str(blockchain.chain[-1])
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif request['action'] == 'get_chain':
                    response = [str(block) for block in blockchain.chain]
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif request['action'] == 'add_transaction':
                    sender = request['sender']
                    receiver = request['receiver']
                    amount = request['amount']
                    description = request['description']
                    transaction = blockchain.add_transaction(sender, receiver, amount, description)
                    response = {'message': 'Transaction added', 'transaction': str(transaction)}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif request['action'] == 'get_balance':
                    try:
                        user = request['user']
                        balance = blockchain.get_balance(user)
                        response = {'message': 'Balance retrieved', 'balance': balance}
                    except Exception as e:
                        response = {'message': f'Error retrieving balance: {str(e)}'}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                else:
                    response = {'message': 'Unknown or unauthorized action'}
                    client_socket.send(json.dumps(response).encode('utf-8'))
            else:
                response = {'message': 'Invalid or missing session token'}
                client_socket.send(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    blockchain = Blockchain(difficulty=2)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("--------------------------")
    print("Server listening on port 5000...")
    print("--------------------------")

    while True:
        client_socket, addr = server.accept()
        print("--------------------------")
        print(f"Connection from {addr}")
        print("--------------------------")
        handle_client(client_socket, blockchain)

if __name__ == "__main__":
    start_server()
