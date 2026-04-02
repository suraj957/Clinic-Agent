from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents import run_agents

app = FastAPI()

class AppointmentRequest(BaseModel):
    message: str

@app.post("/book")
def book_appointment(req: AppointmentRequest):
    try:
        response = run_agents(req.message)
        print("DEBUG RESPONSE:", response) 
        return {"response": response}
    except Exception as e:
        print("ERROR:", e)
        return {"response": f"Error: {str(e)}"}