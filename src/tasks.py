import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
import dateutil
from fastapi import FastAPI, HTTPException
import requests
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import llm


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Allows all origins. Replace "*" with specific domains for better security.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)


Data_dir = "./data"
# root_dir =  "/data"

# Task A1

def run_datagen(user_email: str):
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    subprocess.run(["curl","-O",url], check=True)
    subprocess.run(["python3","datagen.py",user_email, "--root", "./data"], check=True)

def format_md():
    subprocess.run(["npx","prettier@3.4.2","--write",f"{Data_dir}/format.md"],check=True)
    
def count_days():
    data_file = Path("/data/dates.txt")
    output_file = Path("/data/dates-wednesdays.txt")

    # Read dates from file
    with data_file.open("r", encoding="utf-8") as f:
        dates = f.readlines()

    wednesday_count = 0
    error_count = 0

    for date_str in dates:
        date_str = date_str.strip()
        if not date_str:
            continue  # Skip empty lines

        try:
            parsed_date = dateutil.parser.parse(date_str)  # Parse full date

            if parsed_date.weekday() == 2:  # 2 = Wednesday
                wednesday_count += 1
        except Exception as e:
            error_count += 1
            print(f"❌ Skipping invalid date: {date_str} - Error: {e}")

    # Write result to file
    with output_file.open("w", encoding="utf-8") as f:
        f.write(str(wednesday_count) + "\n")

    print(f"\n✅ Total Wednesdays: {wednesday_count}")
    print(f"⚠️ Skipped {error_count} invalid dates")



def sort_contacts():
    contact_file = Path(f"{Data_dir}/contacts.json")
    out_file = Path(f"{Data_dir}/contacts-sorted.json")
    
    with contact_file.open() as f:
        contacts = json.load(f)
    sort_contacts = sorted(contacts, key=lambda x: (x["last_name"],x["first_name"]))
    
    with out_file.open("w") as f:
        json.dump(sort_contacts, f, indent=4)
        
        
def get_recent_logs():
    log_dir = Path(f"{Data_dir}/logs")
    output_file = Path(f"{Data_dir}/logs-recent.txt")
    
    log_files = sorted(log_dir.glob("*.log"), key = os.path.getmtime, reverse = True)[:10]       
        
    with output_file.open("w") as f:
        for log_file in log_files:
            with log_file.open() as lf:
                f.write(lf.readline())
        
        
        
        
def generate_md_index():
    docs_dir = Path(f"{Data_dir}/docs")
    index_file = Path(f"{Data_dir}/docs/index.json")
    index = {}
    
    for md_file in docs_dir.rglob("*.md"):
        relative_path = md_file.relative_to(docs_dir)
        with md_file.open() as f:
            for line in f:
                if line.startswith("# "):
                    index[str(relative_path)] = line[2:].strip()
                    break        

    with index_file.open("w") as f:
        json.dump(index, f , indent=4)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
@app.post("/run_all_tasks")
async def run_all_tasks(user_email: str | None = None):
    try:
        # run_datagen(user_email)
        # format_md()
        # count_days()
        # sort_contacts()
        # get_recent_logs()
        # generate_md_index()
        # llm.extract_email()
        llm.extract_card_number()
        
        return {"status": "All tasks completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
if __name__ == "__main__":
    uvicorn.run("tasks:app", host="127.0.0.1", port=8000, reload=True)

