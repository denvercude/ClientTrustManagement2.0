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