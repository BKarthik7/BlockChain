# client.py

import socket
import json

SERVER_IP = 'localhost'
SERVER_PORT = 5000

session_token = None  

def send_request(action, block_header=None, block_data=None, **kwargs):
    global session_token
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        request = {
            'action': action
        }
        if session_token:
            request['session_token'] = session_token  
        if block_header and block_data:
            request['block_header'] = block_header
            request['block_data'] = block_data

        request.update(kwargs)

        client_socket.send(json.dumps(request).encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        if not response.strip():  
            print("--------------------------")
            print("Error: Received an empty response from the server.")
            print("--------------------------")
            return None
        try:
            response_data = json.loads(response)  
            print("--------------------------")
            print(f"Response: {response_data}")
            print("--------------------------")
            return response_data
        except json.JSONDecodeError:
            print("--------------------------")
            print("Error: Received invalid JSON response from the server.")
            print("--------------------------")
            return None

def add_block(block_header, block_data):
    response = send_request('add_block', block_header, block_data)
    print(f"Add Block Response: {response}")

def get_chain():
    response = send_request('get_chain')
    print(f"Blockchain: {response}")

def login(username, password):
    global session_token
    response = send_request('login', username=username, password=password)
    if response and 'session_token' in response:
        session_token = response['session_token']  
        print("--------------------------")
        print(f"Login Successful: {response}")
        print("--------------------------")
    else:
        print("--------------------------")
        print(f"Login Failed: {response}")
        print("--------------------------")

def add_transaction(sender, receiver, amount, description):
    response = send_request('add_transaction', block_header=None, block_data=None, sender=sender, receiver=receiver, amount=amount, description=description)
    print("--------------------------")
    print(f"Add Transaction Response: {response}")
    print("--------------------------")

def get_balance(user):
    response = send_request('get_balance', block_header=None, block_data=None, user=user)
    print("--------------------------")
    print(f"Balance for {user}: {response}")
    print("--------------------------")

def create_patient(patient_id, patient_data):
    response = send_request('create_patient', patient_id=patient_id, patient_data=patient_data)
    print("--------------------------")
    print(f"Create Patient Response: {response}")
    print("--------------------------")

def add_blood_test(patient_id, blood_test_data):
    response = send_request('add_blood_test', patient_id=patient_id, blood_test_data=blood_test_data)
    print("--------------------------")
    print(f"Add Blood Test Response: {response}")
    print("--------------------------")

def add_prescription(patient_id, prescription_data):
    response = send_request('add_prescription', patient_id=patient_id, prescription_data=prescription_data)
    print("--------------------------")
    print(f"Add Prescription Response: {response}")
    print("--------------------------")

def access_prescription(patient_id):
    response = send_request('access_prescription', patient_id=patient_id)
    print("--------------------------")
    print(f"Access Prescription Response: {response}")
    print("--------------------------")

if __name__ == "__main__":
    login("doctor", "doc123")
    create_patient("patient_001", {"name": "John Doe", "age": 30, "condition": "Fever"})
    add_blood_test("patient_001", {"test": "Blood Test", "result": "Normal"})
    add_prescription("patient_001", {"medication": "Paracetamol", "dosage": "500mg"})
    access_prescription("patient_001")
    add_transaction("doctor", "diagnostic", 50, "Blood test incentive")
    get_balance("doctor")
    add_block("Block 1", "This is the first block.")
    add_block("Block 2", "This is the second block.")
    get_chain()
