from fastapi import FastAPI, HTTPException
from .db import get_connection, add_patient, discharge_patient
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI()

# Define the input schema for adding a patient
class AddPatientRequest(BaseModel):
    first_name: str
    last_name: str
    contract: str

# Define the input schema for discharging a patient
class DischargePatientRequest(BaseModel):
    first_name: str
    last_name: str
    reason_for_discharge: str

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
    """
    Endpoint to discharge a patient.

    Args:
        patient (DischargePatientRequest): The patient data sent in the request body.

    Returns:
        dict: A success message if the patient is discharged successfully.

    Raises:
        HTTPException: If an error occurs while discharging the patient.
    """
    try:
        # Call the function to discharge the patient
        result = discharge_patient(
            patient.first_name, 
            patient.last_name, 
            patient.reason_for_discharge
        )

        # Handle response based on the status
        if result["status"] == "success":
            return {"message": result["message"]}
        elif result["status"] == "failure":
            if "already been discharged" in result["message"]:
                raise HTTPException(status_code=409, detail=result["message"])  # Conflict
            if "No patient found" in result["message"]:
                raise HTTPException(status_code=404, detail=result["message"])  # Not Found
            raise HTTPException(status_code=400, detail=result["message"])  # Other Failure

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=400, detail=f"Error discharging patient: {e}")