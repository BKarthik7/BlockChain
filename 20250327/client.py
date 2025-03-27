# client.py

import socket
import json

SERVER_IP = 'localhost'
SERVER_PORT = 5000

session_token = None  

def send_request(action, block_header=None, block_data=None, **kwargs):
    global session_token
    max_retries = 3
    for attempt in range(max_retries):
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

            response = client_socket.recv(4096).decode('utf-8')
            if not response.strip():
                print(f"Attempt {attempt + 1}/{max_retries}: Empty response from server.")
                if attempt < max_retries - 1:
                    continue  # Retry
                print("--------------------------")
                print("Error: Received an empty response from the server after retries.")
                print("--------------------------")
                return {'error': 'Empty response from server'}
            try:
                response_data = json.loads(response)  
                print("--------------------------")
                print(f"Response: {response_data}")
                print("--------------------------")
                if 'message' in response_data and response_data['message'] == 'Unknown or unauthorized action':
                    print("Error: Unauthorized action or invalid session token.")
                    print(f"Debug Info: Action={action}, Session Token={session_token}, Request={request}")
                return response_data
            except json.JSONDecodeError:
                print("--------------------------")
                print("Error: Received invalid JSON response from the server.")
                print("--------------------------")
                return {'error': 'Invalid JSON response'}

def add_block(block_header, block_data):
    response = send_request('add_block', block_header, {"data": block_data})
    if response and 'error' not in response:
        print(f"Add Block Response: {response}")
    else:
        print("Failed to add block. Debug Info:", response)

def get_chain():
    response = send_request('get_chain')
    if response and 'error' not in response:
        print(f"Blockchain: {response}")
    else:
        print("Failed to retrieve blockchain. Debug Info:", response)

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
    response = send_request('add_transaction', sender=sender, receiver=receiver, amount=amount, description=description)
    if response and 'error' not in response:
        print("--------------------------")
        print(f"Add Transaction Response: {response}")
        print("--------------------------")
    else:
        print("Failed to add transaction. Debug Info:", response)

def get_balance(user=None):
    response = send_request('get_balance')
    if response and 'balance' in response:
        print("--------------------------")
        print(f"Balance: {response['balance']}")
        print("--------------------------")
    else:
        print(f"Failed to retrieve balance. Debug Info: {response}")

def create_patient(patient_id, patient_data):
    response = send_request('create_patient', patient_id=patient_id, patient_data=patient_data)
    print("--------------------------")
    print(f"Create Patient Response: {response}")
    print("--------------------------")

def add_blood_test(patient_id, blood_test_data):
    response = send_request('add_blood_test', patient_id=patient_id, blood_test_data=blood_test_data)
    if response and 'error' not in response:
        print("--------------------------")
        print(f"Add Blood Test Response: {response}")
        print("--------------------------")
    else:
        print("Failed to add blood test. Debug Info:", response)

def add_prescription(patient_id, prescription_data):
    response = send_request('add_prescription', patient_id=patient_id, prescription_data=prescription_data)
    if response and 'error' not in response:
        print("--------------------------")
        print(f"Add Prescription Response: {response}")
        print("--------------------------")
    else:
        print("Failed to add prescription. Debug Info:", response)

def access_prescription(patient_id):
    response = send_request('access_prescription', patient_id=patient_id)
    if response and 'error' not in response:
        print("--------------------------")
        print(f"Access Prescription Response: {response}")
        print("--------------------------")
    else:
        print("Failed to access prescription. Debug Info:", response)

users = {
    "doctor": {"password": "doc123", "role": "doctor", "functions": ["create_patient", "add_prescription", "access_prescription", "add_transaction", "get_balance"]},
    "diagnostic": {"password": "diag123", "role": "diagnostic", "functions": ["add_blood_test"]},
    "pharmacy": {"password": "pharma123", "role": "pharmacy", "functions": ["access_prescription"]},
}

if __name__ == "__main__":
    # login("doctor", "doc123")
    # create_patient("patient_001", {"name": "John Doe", "age": 30, "condition": "Fever"})
    # add_blood_test("patient_001", {"test": "Blood Test", "result": "Normal"})
    # add_prescription("patient_001", {"medication": "Paracetamol", "dosage": "500mg"})
    # access_prescription("patient_001")
    # add_transaction("doctor", "diagnostic", 50, "Blood test incentive")
    # get_balance("doctor")
    # add_block("Block 1", "This is the first block.")
    # add_block("Block 2", "This is the second block.")
    # get_chain()
    print("Which user are you?")
    print("1. Doctor (doctor) \n2. Diagnostic Center (diagnostic) \n3. Pharmacy (pharmacy)")
    user = input("Enter your choice: ")

    if user == "doctor":
        print("You are a doctor.")
        print("You can perform the following actions: \n1. Create Patient \n2. Add Prescription \n3. Access Prescription \n4. Add Transaction \n5. Get Balance")
        action = input("Enter the action you want to perform: ")
        if action == "1":
            patient_id = input("Enter patient ID: ")
            patient_data = input("Enter patient data: ")
            create_patient(patient_id, patient_data)
        elif action == "2":
            patient_id = input("Enter patient ID: ")
            prescription_data = input("Enter prescription data: ")
            add_prescription(patient_id, prescription_data)
        elif action == "3":
            patient_id = input("Enter patient ID: ")
            access_prescription(patient_id)
        elif action == "4":
            sender = input("Enter sender: ")
            receiver = input("Enter receiver: ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            add_transaction(sender, receiver, amount, description)
        elif action == "5":
            get_balance("doctor")
        else:
            print("Invalid action.")
    elif user == "diagnostic":
        print("You are a diagnostic center.")
        print("You can perform the following actions: \n1. Add Blood Test")
        action = input("Enter the action you want to perform: ")
        if action == "1":
            patient_id = input("Enter patient ID: ")
            blood_test_data = input("Enter blood test data: ")
            add_blood_test(patient_id, blood_test_data)
        else:
            print("Invalid action.")
    elif user == "pharmacy":
        print("You are a pharmacy.")
        print("You can perform the following actions: \n1. Access Prescription")
        action = input("Enter the action you want to perform: ")
        if action == "1":
            patient_id = input("Enter patient ID: ")
            access_prescription(patient_id)
        else:
            print("Invalid action.")
    else:
        print("Invalid user.")
