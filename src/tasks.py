import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import dateutil
import duckdb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import markdown
import uvicorn
import httpx
import requests
from pathlib import Path
from PIL import Image
import pytesseract
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import sqlite3
import git
import pandas as pd
import whisper



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # Allows all origins. Replace "*" with specific domains for better security.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)

load_dotenv()

API_KEY = os.getenv("AIR_PROXY_TOKEN")

chat_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

Data_dir = "./data"
# root_dir =  "/data"


# Task A1
def run_datagen(user_email: str):
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    subprocess.run(["curl","-O",url], check=True)
    subprocess.run(["python3","datagen.py",user_email, "--root", "./data"], check=True)
    


def format_md():
    subprocess.run(["npx","prettier@3.4.2","--write",f"{Data_dir}/format.md"],check=True)
    
    
    
def count_wednesdays(source_file,output_file):
    data_file = Path(source_file)
    output_file = Path(output_file)

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
        

def extract_email(source_file, output_file):

    email_file = Path(source_file)
    output_file = Path(output_file)
    with email_file.open("r", encoding="utf-8") as f:
        email_content = f.read()

    prompt = f"Extract only sender's email address from the following email:\n\n{email_content}"

    llm_payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": email_content}
        ]
    }

    response = requests.post(chat_url, headers=headers, json=llm_payload)
    sender_email = response.json()["choices"][0]["message"]["content"].strip()

    with output_file.open("w", encoding="utf-8") as f:
        f.write(sender_email + "\n")

    print(f"✅ Extracted sender email: {sender_email}")


def extract_card_number(image_path,output_file):
    image_file = Path(image_path)
    output_file = Path(output_file)

    image = Image.open(image_file)
    extracted_text = pytesseract.image_to_string(image)

    # cleaned_card_number = "".join(filter(str.isdigit(),extracted_text))
    cleaned_card_number = "".join(
        c for c in extracted_text if c.isdigit())[:12]
    with output_file.open("w", encoding="utf-8") as f:
        f.write(cleaned_card_number + "\n")

    print(f"✅ Extracted Credit Card Number: {cleaned_card_number}")


def find_most_similar_comments(source_file,output_file):
    comments_file = Path(source_file)
    output_file = Path(output_file)

    with comments_file.open("r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    embedding_response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
        headers=headers,
        json={
            "model": "text-embedding-3-small",
            "input": comments
        }
    )

    # -------Debugging Part-------------------------------|
    # response_json = embedding_response.json()           |
    # if "data"  in response_json:                        |
    #     print(f"❌ OpenAI API Error: {response_json}")  |
    #     # return                                        |
    # -------Debugging Part-------------------------------|

    embeddings = np.array([item["embedding"]
                          for item in embedding_response.json()["data"]])

    similarity_matrix = cosine_similarity(embeddings)

    np.fill_diagonal(similarity_matrix, -1)

    i, j = np.unravel_index(np.argmax(similarity_matrix),
                            similarity_matrix.shape)

    with output_file.open("w", encoding="utf-8") as f:
        f.write(comments[i] + "\n" + comments[j] + "\n")
    print(f"✅ Most Similar comments saved to {output_file}")


def calculate_gold_tickets_sales( source_file, output_file):

    DB_FILE = Path(source_file)
    OUTPUT_FILE = Path(output_file)

    if not DB_FILE.exists():
        print("DB file not found")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0]

        total_sales = total_sales if total_sales is not None else 0

        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            f.write(str(total_sales) + "\n")

        print(f"Total 'Gold' ticket sales are: {total_sales}")

    except sqlite3.Error as e:
        print(f"Database Error{e}")
    finally:
        conn.close()
 
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
 
 
 # Task B3
 
def fetch_api_data(api_url,output_file):
    """ Fetches data from an API and saves it as a JSON file. """     
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()   # Raises Error for invalid response
        
        data = response.json()
        
        output_file = Path(output_file)
        
        output_file.write_text(str(data), encoding="utf-8")
        
        print(f"Data Fetched from {api_url} and saved to {output_file}")
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
 
 
 
 # Task B4:
 
def clone_and_commit(repo_url, commit_message = "Automated commit"):
    """ Clones a git repository, makes a commit, and pushes changes. """
    repo_dir = Path("/data/repo")  
    
    if repo_dir.exists():
        print(" Repo already cloned, Skipping Cloning step")
    else:
        git.Repo.clone_from(repo_url, repo_dir)
        print(f"Repo cloned from {repo_url}")
        
    # Making a commit
    
    repo = git.Repo(repo_dir)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name="origin")
    origin.push()
    print(f"Commit pushed: {commit_message}")

# Task B5
def run_sql_query(db_file, query, output_file):
    """Runs and SQL query on SQLite or DuckDB and save results.""" 
    db_file = Path(db_file)
    output_file = Path(output_file)
    
    if not db_file.exists():
        print("DB does not exist.")
        return
    try:
        if db_file.suffix == ".db":
            conn = sqlite3.connect(db_file)
        else:
            conn = duckdb.connect(db_file)
            
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        output_file.write_text(str(results), encoding="utf-8")
        print(f"SQL Query executed and results saved to {output_file} with query {query}")
        
    except Exception as e:
        print(f"SQL Error: {e}")
        
    finally:
        conn.close()
        
# Task B6:

def scrape_website(url, output_file):
 
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        output_file = Path(output_file)
        output_file.write_text(soup.prettify(),encoding="utf-8")
        
    except requests.RequestException as e:
        print(f"Failed to scrape website beacuse of: {e}")
        
# Task B7

def resize_image(image_path, output_path,width=300, height = 300):
    """Resize an image to a specific width and height"""
    img = Image.open(image_path)
    img = img.resize((width,height))
    img.save(output_path)
    
    print(f"Image resized and saved to {output_path}")

# Task B8
def transcribe_audio(audio_path, output_text_file):
    """Transcribes an MP3 file and saves the text."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    
    output_file = Path(output_text_file)
    output_file.write_text(result["text"], encoding="utf-8")
    
    print(f"Transcription saved to {output_file}")
    
# Task B9

def convert_md_to_html(md_file,output_html_file):
    """Convert a Markdown file to HTML."""
    md_content = Path(md_file).read_text(encoding="utf-8")
    html_content = markdown.markdown(md_content)
    
    output_file = Path(output_html_file)
    output_file.write_text(html_content, encoding="utf-8")
    
    print(f"Markdown converted HTML and saved to {output_file}")
    

#Task B10


def filter_csv(csv_file,filter_column, filter_value, output_json_file):
    """Filters a CSV file by column and saves it as JSON"""
    df = pd.read_csv(csv_file)
    filtered_df = df[df[filter_column] == filter_value]
    
    output_file = Path(output_json_file)
    filtered_df.to_json(output_file, orient = "records", indent = 4)
    
    print(f"Filtered CSV saved as JSON to {output_json_file}")

 
 
 
 
 
 
 
 
 
 
 
 
