import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime

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

def add_patient(first_name, last_name, contract):
    """
    Add a new patient to the database.
    First checks for existing patient based on name, and generates a new client ID.
    The phase is always set to 1 for new patients.
    A journal entry is also created in the Transactions table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if a patient with the same first and last name already exists
        cursor.execute(
            """
            SELECT ClientID FROM Clients 
            WHERE FirstName = ? AND LastName = ?
            """,
            (first_name, last_name)
        )
        existing_patient = cursor.fetchone()

        if existing_patient:
            print(
                f"Patient '{first_name} {last_name}' is already in the database. "
                "Check records for duplicate name and manually enter the patient if necessary."
            )
            return

        # Generate a new ClientID by finding the max in the Clients table and adding 1
        cursor.execute("SELECT MAX(ClientID) FROM Clients")
        max_client_id = cursor.fetchone()[0]
        new_client_id = (max_client_id + 1) if max_client_id else 1

        # Add the new patient to the database with Phase set to 1
        cursor.execute(
            """
            INSERT INTO Clients (ClientID, FirstName, LastName, Phase, Discharged, Contract)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (new_client_id, first_name, last_name, 1, False, contract)
        )

        # Generate a transaction entry for "Beginning Balance"
        # Find the next transaction ID
        cursor.execute("SELECT MAX(TransactionID) FROM Transactions")
        max_transaction_id = cursor.fetchone()[0]
        new_transaction_id = (max_transaction_id + 1) if max_transaction_id else 1

        # Get today's date in the required format
        transaction_date = datetime.now().strftime("%m/%d/%Y")

        # Insert the transaction entry
        cursor.execute(
            """
            INSERT INTO Transactions (
                TransactionID, TransactionDate, TransactionDescription,
                DepositAmount, WithdrawalAmount, ClientID
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (new_transaction_id, transaction_date, "Beginning Balance", 0, 0, new_client_id)
        )

        # Commit the transaction
        conn.commit()

        print(f"Patient '{first_name} {last_name}' added successfully with ClientID {new_client_id} and Phase 1.")
        print(f"Transaction '{new_transaction_id}' created with description 'Beginning Balance'.")

    except pyodbc.Error as e:
        print(f"Error adding patient: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def discharge_patient(first_name, last_name, reason_for_discharge):
    """
    Discharge a patient by updating the Discharged column to True and adding a journal entry in Transactions.

    Args:
        first_name (str): First name of the patient.
        last_name (str): Last name of the patient.
        reason_for_discharge (str): Reason for discharge (used in the transaction description).

    Returns:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if a patient with the same first and last name exists and is already discharged
        cursor.execute(
            """
            SELECT ClientID, Phase FROM Clients
            WHERE FirstName = ? AND LastName = ?
            """,
            (first_name, last_name)
        )
        patient = cursor.fetchone()

        if not patient:
            print(f"No patient found with the name '{first_name} {last_name}'.")
            return

        client_id, phase = patient

        # Check if the patient is already discharged.
        if phase == 4:
            print(f"Patient '{first_name} {last_name}' has already been discharged.")
            return

        # Update the patient's Discharged status to True
        cursor.execute(
            """
            UPDATE Clients
            SET Phase = 4
            WHERE ClientID = ?
            """,
            (client_id)
        )

        # Generate a transaction entry for the discharge
        # Find the next transaction ID
        cursor.execute("SELECT MAX(TransactionID) FROM Transactions")
        max_transaction_id = cursor.fetchone()[0]
        new_transaction_id = (max_transaction_id + 1) if max_transaction_id else 1

        # Get today's date in the required format
        transaction_date = datetime.now().strftime("%m/%d/%Y")

        # Insert the transaction entry
        cursor.execute(
            """
            INSERT INTO Transactions (
                TransactionID, TransactionDate, TransactionDescription,
                DepositAmount, WithdrawalAmount, ClientID
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (new_transaction_id, transaction_date, reason_for_discharge, 0, 0, client_id)
        )

        # Commit the transaction
        conn.commit()

        print(f"Patient '{first_name} {last_name}' has been discharged successfully.")
        print(f"Transaction '{new_transaction_id}' created with description '{reason_for_discharge}'.")

    except pyodbc.Error as e:
        print(f"Error discharging patient: {e}")
        raise
    finally:
        cursor.close()
        conn.close()