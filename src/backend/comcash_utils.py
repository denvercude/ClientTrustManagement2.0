from .api_client import APIClient
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("ACCESS_DB_PATH")
CONNECTION_STRING = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    f"DBQ={DB_PATH};"
)

def get_connection():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise

def get_current_accounts():
    client = APIClient()

    status = 1
    customer_type = 4
    
    response = client.get_customer_list(status, customer_type)

    if response:
        accounts = [
            {
                "lastName": account.get("lastName", ""),
                "firstName": account.get("firstName", ""),
                "storeCredit": account.get("storeCredit", "0.00")
            }
            for account in response
        ]
        return accounts
    else:
        return []
    
def get_new_accounts():
    client = APIClient()
    cursor = get_connection().cursor()

    query = '''
        SELECT FirstName, LastName, Phase
        FROM Balance
        WHERE Phase = '1';
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    deleted_customer_list = client.get_customer_list(2, 4)
    active_customer_list = client.get_customer_list(1, 4)

    all_customers = {
        (customer['firstName'], customer['lastName'])
        for customer in deleted_customer_list + active_customer_list
    }

    new_accounts = []
    for row in rows:
        first_name, last_name, phase = row
        if (first_name, last_name) not in all_customers:
            new_accounts.append({'firstName': first_name, 'lastName': last_name})

    return new_accounts

def add_new_accounts():
    client = APIClient()
    cursor = get_connection().cursor()

    query = '''
        SELECT FirstName, LastName, Phase
        FROM Balance
        WHERE Phase = '1';
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Fetch the customer lists
    deleted_customer_list = client.get_customer_list(2, 4)
    active_customer_list = client.get_customer_list(1, 4)

    if deleted_customer_list is None or active_customer_list is None:
        print("Failed to fetch customer lists.")
        return []

    all_customers = {
        (customer['firstName'], customer['lastName'])
        for customer in deleted_customer_list + active_customer_list
    }

    new_accounts = []
    for row in rows:
        first_name, last_name, phase = row
        if (first_name, last_name) not in all_customers:
            new_accounts.append({'firstName': first_name, 'lastName': last_name})

    successfully_added_accounts = []
    for account in new_accounts:
        try:
            # Create the new customer
            print(f"Creating customer: {account['firstName']} {account['lastName']}")
            new_customer = client.create_new_customer(
                first_name=account['firstName'],
                last_name=account['lastName']
            )
            
            if new_customer and "id" in new_customer:
                # Update customer type
                print(f"Updating customer type for: {account['firstName']} {account['lastName']}")
                client.update_customer_type(new_customer.get("id"))
                successfully_added_accounts.append(account)
            else:
                print(f"Failed to create customer for: {account['firstName']} {account['lastName']}")
        except Exception as e:
            print(f"Error processing account {account['firstName']} {account['lastName']}: {e}")

    return successfully_added_accounts