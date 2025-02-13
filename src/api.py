from SYS_MSG import SYSTEM_MESSAGE
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
from tasks import *
from functions import function_list


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
    



# @app.post("/run")
# async def run_task(task: str):
#     """Processes tasks using OpenAI function calling."""
#     try:
#         payload = {
#             "model": "gpt-4o-mini",
#             "messages": [
#                 {"role": "system", "content": SYSTEM_MESSAGE},
#                 {"role": "user", "content": task}
#             ],
#             "tools": tools,
#             "tool_choice": "auto"
#         }

#         response = requests.post(chat_url, headers=headers, json=payload)
#         response_json = response.json()

#         # 🔴 Debugging: Print Full Response
#         print("🔎 FULL OPENAI RESPONSE:", json.dumps(response_json, indent=4))

        
#         tool_calls = response_json["choices"][0]["message"].get(
#             "tool_calls", [])
        
#         # content = response_json["choices"][0]["message"].get("content", "")
#         if not tool_calls:
#             raise HTTPException(
#                 status_code=400, detail="No function identified")

#         # ✅ Convert JSON string into Python dictionary
#         function_data = tool_calls[0]["function"]
#         function_name = function_data["name"]
#         function_args = json.loads(function_data["arguments"])
        
    
#         print(f"🔎 Extracted Function Call: {function_name}")

#         if function_name not in globals() or not callable(globals()[function_name]):
#             raise HTTPException(
#                 status_code=400, detail=f"Unknown function: {function_name}")


        
#         result = globals()[function_name](**function_args)
#         try:
#             result_json = json.loads(json.dumps(result, default=str))
#         except TypeError as e:
#             raise HTTPException(
#             status_code=500, detail=f"Serialization error: {str(e)}")
        
#         return {
#             "task": task,
#             "status": "Completed successfully",
#             "executed_function": function_name,
#             # Ensure JSON serializability
#             "result": result_json
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/run")
async def run_task(task: str):
    """Processes tasks using OpenAI function calling."""
    function_list = list(AVAILABLE_FUNCTIONS.values())
    try:
      
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": task}
            ],
            "functions": function_list,
            "function_call": "auto"
        }

        response = httpx.post(chat_url, headers=headers, json=payload)
        response_json = response.json()

        print("🔎 FULL OPENAI RESPONSE:", json.dumps(response_json, indent=4))
        
        # message = response_json["choices"][0]["message"]
        content = response_json["choices"][0]["message"].get("content", "")
        function_data = json.loads(content)
        function_name = function_data.get("function")
        function_args = function_data.get("params", {})

        if not function_name:
            raise HTTPException(
                status_code=400, detail="No function call detected.")
            
        if function_name.startswith("functions."):
             function_name = function_name.split(".")[-1]
             
        if function_name not in globals():
            raise HTTPException(
                status_code=400, detail=f"Unknown function: {function_name}")

        print(f"🔎 OpenAI Selected Function: {function_name}")
        print(f"🔎 Arguments: {function_args}")
        
        
        # Directly execute function (you need to implement the actual function logic)
        result = globals()[function_name](
            **function_data.get("parameters", {}))

        # execution_result = AVAILABLE_FUNCTIONS[function_name](**function_args)
        return {"task": task, "executed_function": function_name, "result": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in function execution: {str(e)}")



    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
