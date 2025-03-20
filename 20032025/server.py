# server.py

import socket
import json
from blockchain import Blockchain

def handle_client(client_socket, blockchain):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break

            
            request = json.loads(data)

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

            else:
                response = {'message': 'Unknown action'}
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
    print("Server listening on port 5000...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket, blockchain)

if __name__ == "__main__":
    start_server()
