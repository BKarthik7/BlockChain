# client.py

import socket
import json

SERVER_IP = 'localhost'
SERVER_PORT = 5000

def send_request(action, block_header=None, block_data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        request = {
            'action': action
        }
        if block_header and block_data:
            request['block_header'] = block_header
            request['block_data'] = block_data

        client_socket.send(json.dumps(request).encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print("Response:", response)

def add_block(block_header, block_data):
    send_request('add_block', block_header, block_data)

def get_chain():
    send_request('get_chain')

if __name__ == "__main__":

    add_block("Block 1", "This is the first block.")
    add_block("Block 2", "This is the second block.")
    get_chain()
