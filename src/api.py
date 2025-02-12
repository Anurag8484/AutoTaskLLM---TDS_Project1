import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
from tasks import *


load_dotenv()

API_KEY = os.getenv("AIR_PROXY_TOKEN")

chat_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

AVAILABLE_FUNCTIONS = {
    "count_wednesdays": {
        "name": "count_wednesdays",
        "description": "Count the number of Wednesdays in a given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing dates."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
            },
            "required": ["source_file", "output_file"]
        }
    },
    "calculate_gold_sales": {
        "name": "calculate_gold_sales",
        "description": "Calculate total sales for Gold tickets.",
        "parameters": {
            "type": "object",
            "properties": {
                "db_file": {"type": "string", "description": "Path to the SQLite database file."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
            },
            "required": ["db_file", "output_file"]
        }
    },
    "fetch_api_data": {
        "name": "fetch_api_data",
        "description": "Fetch data from an API and save it.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {"type": "string", "description": "URL of the API to fetch data from."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
            },
            "required": ["api_url", "output_file"]
        }
    }
}





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Allows all origins. Replace "*" with specific domains for better security.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)

@app.post("/run_all_tasks")
async def run_all_tasks(user_email: str | None = None):
    try:
        # run_datagen(user_email)
        # format_md()
        # count_days()
        # sort_contacts()
        # get_recent_logs()
        # generate_md_index()
        # extract_email()
        # extract_card_number()
        # find_most_similar_comments()
        # calculate_gold_tickets_sales()

        return {"status": "All tasks completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/run")
async def run_task(request: dict):
    """
    Test functions manually by sending function name and parameters.
    Example:
    {
        "function": "count_wednesdays",
        "parameters": {
            "source_file": "/data/dates.txt",
            "output_file": "/data/wednesdays_count.txt"
        }
    }
    """
    try:
        function_name = request.get("function")
        function_args = request.get("parameters", {})

        if not function_name or function_name not in globals():
            raise HTTPException(
                status_code=400, detail=f"Unknown function: {function_name}")

        # Execute function dynamically
        result = globals()[function_name](**function_args)

        return {"status": "Function executed successfully", "function": function_name, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
