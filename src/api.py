from pathlib import Path
import subprocess
import json
import re
from SYS_MSG import S2, SYSTEM_MESSAGE
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
@app.get("/read")
async def read_file(path: str):
    """Returns the content of a specified file if it exists within /data/"""
    DATA_DIR = Path("data")
    file_path = DATA_DIR / Path(path).name  # Restrict path to `/data/`

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return {"content": file_path.read_text(encoding="utf-8")}

   
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
        
#         tool_calls = response_json["choices"][0]["message"].get("function_call", {})

#         if not tool_calls:
#             raise HTTPException(status_code=400, detail="No function call detected.")

#         function_name = tool_calls.get("name")
#         raw_args = tool_calls.get("arguments", "{}")

#         try:
#             function_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
#         except json.JSONDecodeError:
#             raise HTTPException(status_code=500, detail="Invalid JSON format in function arguments.")

#         if function_name.startswith("functions."):
#             function_name = function_name.split(".")[-1]

#         if function_name not in globals():
#             raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")

#         print(f"🔎 OpenAI Selected Function: {function_name}")
#         print(f"🔎 Arguments: {function_args}")

#         # Execute the function
#         result = globals()[function_name](**function_args)

#         return {"task": task, "executed_function": function_name, "result": result}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in function execution: {str(e)}")


app = FastAPI()

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure API key is set

SYSTEM_MESSAGE = """
You are an AI-powered automation agent that generates and executes Python code dynamically.
- Ensure the generated code is **fully executable** without manual modifications.
- If an error occurs, analyze the **error message and input file format** and **fix the issue automatically**.
- Read the input file before processing to detect its format.
- Do **not** generate explanations, just executable Python code.
- Ensure file paths remain within `/data/`.
- If a task is unclear, return "unknown_task".
"""


def execute_python_code(code: str):
    """Saves and executes Python code, returning output or errors."""
    temp_file = "generated_task.py"

    with open(temp_file, "w") as f:
        f.write(code)

    result = subprocess.run(["python3", temp_file],
                            capture_output=True, text=True)
    return result.stdout, result.stderr


@app.post("/run")
async def run_task(task: str):
    """Processes a task by generating, executing, and self-correcting Python code."""
    try:
        # 🔹 1️⃣ Generate Initial Code
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": S2},
                {"role": "user", "content": f"Write a Python script to: {task}"}
            ],
            "temperature": 0
        }

        headers = {"Authorization": f"Bearer {API_KEY}",
                   "Content-Type": "application/json"}
        response = requests.post(chat_url, headers=headers, json=payload)
        response_json = response.json()

        # 🔍 Extract generated code
        code = response_json["choices"][0]["message"]["content"]
        code = re.sub(r"^```python\n|```$", "", code,
                      flags=re.MULTILINE).strip()

        # 🔥 2️⃣ Execute Initial Code
        output, error = execute_python_code(code)

        # ✅ Success Case
        if not error:
            return {"task": task, "status": "Completed", "output": output}

        # 🔄 3️⃣ If Error Occurs → Ask OpenAI to Fix
        print(f"❌ Error Detected: {error}")

        fix_payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": S2},
                {"role": "user", "content": f"The following Python script failed:\n\n{code}\n\nError:\n{error}\n\nFix the issue and return corrected code."}
            ],
            "temperature": 0
        }

        fix_response = requests.post(
            OPENAI_API_URL, headers=headers, json=fix_payload)
        fix_response_json = fix_response.json()

        # 🔍 Extract Fixed Code
        fixed_code = fix_response_json["choices"][0]["message"]["content"]
        fixed_code = re.sub(
            r"^\s*```[\w]*\n|\s*```$", "", fixed_code, flags=re.MULTILINE).strip()
        print(fixed_code)  # Debug output


        # 🔥 4️⃣ Execute Fixed Code
        final_output, final_error = execute_python_code(fixed_code)

        if not final_error:
            return {"task": task, "status": "Completed After Fix", "output": final_output}
        else:
            return {"task": task, "status": "Failed", "error": final_error}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Critical Error: {str(e)}")

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
