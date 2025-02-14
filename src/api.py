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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Allows all origins. Replace "*" with specific domains for better security.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)


def normalize_path(file_path: str) -> str:
    """
    Converts '/data/' paths to './data/' for compatibility with the evaluation system.
    """
    if file_path.startswith("/data/"):
        # Replace /data/ with ./data/
        return str(Path("./data") / file_path[6:])
    return file_path

# @app.post("/run_all_tasks")
# async def run_all_tasks(user_email: str | None = None):
#     try:
#         # run_datagen(user_email)
#         # format_md()
#         # count_days()
#         # sort_contacts()
#         # get_recent_logs()
#         # generate_md_index()
#         # extract_email()
#         # extract_card_number()
#         # find_most_similar_comments()
#         # calculate_gold_tickets_sales()

#         return {"status": "All tasks completed successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/run")
async def run_task(task: str):
    """Processes tasks using OpenAI function calling."""
    Lfunctions = list(function_list.values())
    try:
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": task}
            ],
            "functions": Lfunctions,
            "function_call": "auto"
        }

        response = httpx.post(chat_url, headers=headers, json=payload)
        response_json = response.json()

        print("🔎 FULL OPENAI RESPONSE:", json.dumps(response_json, indent=4))
        
        tool_calls = response_json["choices"][0]["message"].get("function_call", {})

        if not tool_calls:
            raise HTTPException(status_code=400, detail="No function call detected.")

        function_name = tool_calls.get("name")
        raw_args = tool_calls.get("arguments", "{}")

        try:
            function_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON format in function arguments.")

        if function_name.startswith("functions."):
            function_name = function_name.split(".")[-1]

        if function_name not in globals():
            raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")

        print(f"🔎 OpenAI Selected Function: {function_name}")
        print(f"🔎 Arguments: {function_args}")

        # Execute the function
        result = globals()[function_name](**function_args)

        return {"task": task, "executed_function": function_name, "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in function execution: {str(e)}")
  
# @app.post("/run")
# async def run_task(task: str):
#     """Processes tasks using OpenAI function calling."""
#     Lfunctions = list(function_list.values())
#     try:
      
#         payload = {
#             "model": "gpt-4o-mini",
#             "messages": [
#                 {"role": "system", "content": SYSTEM_MESSAGE},
#                 {"role": "user", "content": task}
#             ],
#             "functions": Lfunctions,
#             "function_call": "auto"
#         }

#         response = httpx.post(chat_url, headers=headers, json=payload)
#         response_json = response.json()

#         print("🔎 FULL OPENAI RESPONSE:", json.dumps(response_json, indent=4))
        
#         # message = response_json["choices"][0]["message"]
#         content = response_json["choices"][0]["message"].get("content", "")
#         function_data = json.loads(content)
#         function_name = function_data.get("function")
#         raw_args = function_data.get("parameters") or function_data.get(
#                     "params") or function_data.get("arguments") or "{}"
#         try:
#             function_args = json.loads(raw_args) if isinstance(
#                 raw_args, str) else raw_args
#         except json.JSONDecodeError:
#             raise HTTPException(
#                 status_code=500, detail="Invalid JSON format in function arguments")

#         if not function_name:
#             raise HTTPException(
#                 status_code=400, detail="No function call detected.")
            
#         if function_name.startswith("functions."):
#              function_name = function_name.split(".")[-1]
             
#         if function_name not in globals():
#             raise HTTPException(
#                 status_code=400, detail=f"Unknown function: {function_name}")

#         print(f"🔎 OpenAI Selected Function: {function_name}")
#         print(f"🔎 Arguments: {function_args}")
#         for key, value in function_args.items():
#             if isinstance(value, str) and value.startswith("/data/"):
#                 function_args[key] = normalize_path(value)
        
#         print(f"🔎 Arguments after Normaliztion: {function_args}")
        
#         # Directly execute function (you need to implement the actual function logic)
#         result = globals()[function_name](**function_args)


#         # execution_result = AVAILABLE_FUNCTIONS[function_name](**function_args)
#         return {"task": task, "executed_function": function_name, "result": result}

#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error in function execution: {str(e)}")



    
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
