from src.config import API_KEY, API_PIN, API_PASSWORD, API_URL
import json
import os
import requests
import time

class APIClient:
    def __init__(self, token_file="token_data.json"):
        self.api_key = API_KEY
        self.pin = API_PIN
        self.password = API_PASSWORD
        self.signin_url = f"{API_URL}/employee/auth/signin"
        self.customer_list_url = f"{API_URL}/employee/customer/list"
        self.create_customer_url = f"{API_URL}/employee/customer/create"
        self.update_customer_url = f"{API_URL}/employee/customer/update"
        self.update_balance_url = f"{API_URL}/employee/customer/updatePoints"
        self.delete_customer_url = f"{API_URL}/employee/customer/delete"
        self.get_sales_url = f"{API_URL}/employee/customer/sales"
        self.token_file = token_file
        self.token = None
        self.token_expiration = None
        self.load_token_from_file()

    def load_token_from_file(self):
        # Load token and expiration from a file if it exists
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                self.token = data.get("token")
                self.token_expiration = data.get("token_expiration")
                print("Loaded token from file.")
        else:
            print("No token file found. Need to authenticate.")

    def save_token_to_file(self):
        # Save token and expiration to a file
        data = {
            "token": self.token,
            "token_expiration": self.token_expiration
        }
        with open(self.token_file, 'w') as file:
            json.dump(data, file)
        print("Token saved to file.")

    def authenticate(self):
        # Request a new bearer token
        payload = json.dumps({
            "openApiKey": self.api_key,
            "pin": self.pin,
            "password": self.password
        })
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.signin_url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            print(data)
            self.token = data.get("accessToken")
            expires_in = data.get("expiresIn")
            print(f"Expires in: {expires_in}")
            self.token_expiration = expires_in  # Track token expiration in seconds
            self.save_token_to_file()  # Save token to file after successful authentication
            print("Authenticated successfully. Token received.")
        else:
            print(f"Failed to authenticate. Status Code: {response.status_code}")

    def is_token_valid(self):
        # Check if token exists and hasn't expired
        if self.token and float(self.token_expiration) > time.time():
            return True
        return False

    def get_customer_list(self, status, customer_type):
        if not self.is_token_valid():
            print("Token expired or invalid. Authenticating...")
            self.authenticate()

        if self.token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            payload = json.dumps({
                "limit": 100000,
                "order": "asc",
                "type": customer_type,
                "status": status
            })

            response = requests.post(self.customer_list_url, headers=headers, data=payload)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch customer list. Status Code: {response.status_code}")
                return None
    
    def create_new_customer(self, first_name, last_name):
        if not self.is_token_valid():
            print("Token expired or invalid. Authenticating...")
            self.authenticate()

        if self.token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            payload = json.dumps({
                "countryPhoneCode": 1,
                "phone": 0000000000,
                "firstName": first_name,
                "lastName": last_name,
                "locationId": 1
            })

            response = requests.post(self.create_customer_url, headers=headers, data=payload)

            if response.status_code == 200:
                print("Customer created successfully.")
                return response.json()
            else:
                print(f"Failed to create customer. Status Code: {response.status_code}")
                return None
    
    def update_customer_type(self, customer_id):
        if not self.is_token_valid():
            print("Token expired or invalid. Authenticating...")
            self.authenticate()

        if self.token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            payload = json.dumps({
                "id": customer_id,
                "typeId": "4"
            })

            response = requests.post(self.update_customer_url, headers=headers, data=payload)

            if response.status_code == 200:
                print("Customer type updated successfully.")
                return response.json()
            else:
                print(f"Failed to update customer type. Status Code: {response.status_code}")
                return None