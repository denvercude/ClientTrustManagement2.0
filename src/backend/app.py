from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .db import get_connection, add_patient, discharge_patient, update_phase
from .excel_utils import create_deposits_sheet
from pydantic import BaseModel
import pandas as pd
import logging
from .api_client import APIClient
from .comcash_utils import get_current_accounts, get_new_accounts


app = FastAPI()


class AddPatientRequest(BaseModel):
    first_name: str
    last_name: str
    contract: str


class DischargePatientRequest(BaseModel):
    first_name: str
    last_name: str
    reason_for_discharge: str

class UpdatePhaseRequest(BaseModel):
    first_name: str
    last_name: str
    new_phase: int

class CreateDepositRequest(BaseModel):
    deposits: list

# Root endpoint to provide a welcome message
@app.get("/")
async def root():
    """
    Root endpoint for the Client Trust Management API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Client Trust Management API"}

# Endpoint to test database connectivity
@app.get("/test-db")
async def test_db():
    """
    Endpoint to test the database connection.

    Returns:
        dict: A success message if the connection is successful,
              or an error message if the connection fails.
    """
    try:
        # Attempt to establish and close a database connection
        conn = get_connection()
        conn.close()
        return {"message": "Database connection successful!"}
    except Exception as e:
        # Return an error message if the connection fails
        return {"error": str(e)}

# Endpoint to add a new patient to the database
@app.post("/add-patient/")
async def add_patient_endpoint(patient: AddPatientRequest):
    """
    Endpoint to add a new patient to the system.
    Args:
        patient (AddPatientRequest): The patient data sent in the request body.
    Returns:
        dict: A success message or error message.
    """
    try:
        # Add patient information to the database
        result = add_patient(patient.first_name, patient.last_name, patient.contract)

        # Return appropriate response based on the result
        if result["status"] == "success":
            return {"message": result["message"]}
        elif result["status"] == "failure":
            raise HTTPException(status_code=409, detail=result["message"])  # Conflict
        else:
            raise HTTPException(status_code=500, detail="Unexpected error occurred.")
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=400, detail=f"Error adding patient: {e}")

# Endpoint to discharge an existing patient
@app.put("/discharge-patient/")
async def discharge_patient_endpoint(patient: DischargePatientRequest):
    try:
        result = discharge_patient(
            patient.first_name, 
            patient.last_name, 
            patient.reason_for_discharge
        )

        if result["status"] == "success":
            return {"message": result["message"]}
        elif result["status"] == "failure":
            if "already been discharged" in result["message"]:
                raise HTTPException(status_code=409, detail=result["message"])
            if "No patient found" in result["message"]:
                raise HTTPException(status_code=404, detail=result["message"])
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException as http_exc:
        # Reraise known HTTP exceptions
        raise http_exc
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=400, detail=f"Error discharging patient: {e}")
    
@app.put("/update-phase/")
async def update_phase_endpoint(patient: UpdatePhaseRequest):
    """
    Endpoint to update the phase for an existing patient.
    Args:
        patient (UpdatePhaseRequest): The patient data sent in the request body.
    Returns:
        dict: A success message or error message.
    """
    try:
        # Call the update_phase function with input data
        result = update_phase(
            patient.first_name,
            patient.last_name,
            patient.new_phase
        )

        # Handle success and failure cases
        if result["status"] == "success":
            return {"message": result["message"]}
        elif result["status"] == "failure":
            if "already in phase" in result["message"]:
                raise HTTPException(status_code=409, detail=result["message"])
            if "No patient found" in result["message"]:
                raise HTTPException(status_code=404, detail=result["message"])
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException as http_exc:
        # Reraise known HTTP exceptions
        raise http_exc
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=400, detail=f"Error updating phase: {e}")
    
@app.post("/create-deposits/")
async def create_deposits(deposit_data: CreateDepositRequest, request: Request):
    try:
        logging.info(f"Received request at {request.url} with data: {deposit_data.deposits}")
        if not deposit_data.deposits or not isinstance(deposit_data.deposits, list):
            raise ValueError("Invalid deposit data: expected a non-empty list of deposits.")
        df = pd.DataFrame(deposit_data.deposits)
        logging.info(f"DataFrame created with {len(df)} entries.")
        response = create_deposits_sheet(df)
        logging.info("Deposit sheet successfully created.")
        return JSONResponse(status_code=200, content=response)
    except ValueError as ve:
        logging.error(f"Value error: {str(ve)}")
        raise HTTPException(status_code=400, detail={"message": str(ve)})
    except FileNotFoundError as fnfe:
        logging.error(f"File not found: {str(fnfe)}")
        raise HTTPException(status_code=404, detail={"message": str(fnfe)})
    except Exception as e:
        logging.error(f"Unexpected server error: {str(e)}")
        raise HTTPException(status_code=500, detail={"message": str(e)})

@app.get("/current-accounts/")
async def get_current_accounts_endpoint():
    """
    Endpoint to retrieve current accounts with status 1 and customer_type 4.
    Returns:
        dict: List of current accounts or an error message.
    """
    try:
        # Call the function from comcash_utils
        accounts = get_current_accounts()
        return {"accounts": accounts}
    except RuntimeError as e:
        # Handle runtime errors from the utility function
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/new-accounts/")
async def get_current_accounts_endpoint():
    """
    Endpoint to retrieve accounts to be added.
    Returns:
        dict: List of current accounts or an error message.
    """
    try:
        # Call the function from comcash_utils
        accounts = get_new_accounts()
        return {"accounts": accounts}
    except RuntimeError as e:
        # Handle runtime errors from the utility function
        raise HTTPException(status_code=500, detail=str(e))