from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import requests
import os

# Initializing the FastAPI app

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Allows all origins. Replace "*" with specific domains for better security.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)
@app.get("/read")
async def read_file(path: str):
    """ Returns the content of the specified file """
    
    file_path = Path(path)
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404,detail="File not found")
    return {"content":file_path.read_text(encoding="utf-8")}

@app.post("/run")
async def run_task(task: str,user_email:str):
    """ Processess the given task description and execute it """
    # Datagen files downloading
    
    if "run dataget.py" in task.lower():
        try:
            run_datagen(user_email)
            return {"task":task,"status":"Success"}
        except Exception as e:
            raise HTTPException(status_code=500,detail=str(e))
    
    return {"task":task,"status":"Processing soon..."}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
