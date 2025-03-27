# client.py

import socket
import json

SERVER_IP = 'localhost'
SERVER_PORT = 5000

def send_request(action, block_header=None, block_data=None, **kwargs):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        request = {
            'action': action
        }
        if block_header and block_data:
            request['block_header'] = block_header
            request['block_data'] = block_data

        request.update(kwargs)

        client_socket.send(json.dumps(request).encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print("Response:", response)

def add_block(block_header, block_data):
    send_request('add_block', block_header, block_data)

def get_chain():
    send_request('get_chain')

def login(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        request = {'action': 'login', 'username': username, 'password': password}
        client_socket.send(json.dumps(request).encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print("Response:", response)

def add_transaction(sender, receiver, amount, description):
    send_request('add_transaction', block_header=None, block_data=None, sender=sender, receiver=receiver, amount=amount, description=description)

def get_balance(user):
    send_request('get_balance', block_header=None, block_data=None, user=user)

if __name__ == "__main__":
    login("doctor", "doc123")
    add_transaction("doctor", "diagnostic", 50, "Blood test incentive")
    get_balance("doctor")
    add_block("Block 1", "This is the first block.")
    add_block("Block 2", "This is the second block.")
    get_chain()
