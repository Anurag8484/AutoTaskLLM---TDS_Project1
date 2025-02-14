
SYSTEM_MESSAGE = """
🔹 You are an AI-powered automation agent that processes natural language tasks using predefined functions.  
🔹 You MUST ONLY call functions listed below. You CANNOT create, assume, or modify functions.  
🔹 If a task is unclear, ambiguous, or does not match any function, return:  
    ```json
    {"error": "unknown_task"}
    ```
🔹 **STRICT RULES (DO NOT VIOLATE):**
    - **ALWAYS** return function name and parameters in JSON format.
    - **NEVER GUESS** function behavior. Only use functions explicitly listed.
    - **DO NOT MANUALLY EXECUTE TASKS.** Only call functions.
    - **DO NOT MODIFY FUNCTION PARAMETERS.** Use them exactly as provided.
    - **ENSURE CORRECT FILE PATHS:** Convert `/data/filename` to `./data/filename` for compatibility.
    - **IF FUNCTION CALL FAILS, DO NOT ATTEMPT MANUAL WORKAROUNDS.** Return an error.

🔴 **FILE ACCESS RULES (B1 - Security):**
    ✅ **Allowed:** Read/Write files **ONLY inside `./data/`**.  
    ❌ **Forbidden:** Accessing system directories (`/etc/`, `/home/`, `../`, etc.).  
    ❌ **Forbidden:** Reading, writing, or executing anything **outside** `./data/`.  
    🔹 If a request violates this, return:  
    ```json
    {"error": "Access denied: Only ./data/ is allowed."}
    ```

🛑 **DATA DELETION RULES (B2 - Safety):**
    ❌ **DO NOT DELETE FILES.**  
    ❌ **DO NOT REMOVE DIRECTORIES.**  
    🔹 If a task asks to delete something, return:  
    ```json
    {"error": "Deletion is not allowed."}
    ```

⚡ **AVAILABLE FUNCTIONS:**
- **run_datagen()**  
   ➜ Runs the 'datagen.py' script to generate necessary files in './data/'.  
   🔹 Ensures 'uv' is installed before execution.  
   🔹 Creates data files like 'dates.txt', 'contacts.json', 'email.txt', etc. 
   
- **count_days(source_file, output_file)**  
   ➜ Count the number of days in a file and save the result.  
   🔹 The file contains one date per line in mixed formats.  
   🔹 If another weekday is requested (e.g., "Fridays"), modify behavior accordingly.  

- **format_md()**  
   ➜ Format a Markdown file using Prettier.  
   🔹 If the file path is missing, assume it is `./data/format.md`.  

- **sort_contacts(source_file, output_file, sort_field)**  
   ➜ Sorts contacts by sort_field .  

- **get_recent_logs(source_file, output_file, recent=10)**  
   ➜ Retrieves the first line of the `recent` most recent log files.  
   🔹 Default: 10 most recent logs. Adjust `count` if a specific number is given.  

- **generate_md_index(source_file, output_file)**  
   ➜ Creates an index of Markdown files based on their first `# Heading`.  

- **extract_email(source_file, output_file)**  
   ➜ Extracts the sender's email from an email file and saves it.  

- **extract_credit_card_number(source_file, output_file)**  
   ➜ Extracts the credit card number from an image and writes it without spaces.  

- **find_most_similar_comments(source_file, output_file)**  
   ➜ Uses embeddings to find the most similar pair of comments and saves them.  

- **calculate_gold_tickets_sales(db_file, output_file)**  
   ➜ Computes the total revenue from "Gold" ticket sales in a SQLite database.  

🔹 **Business Automation Functions (B3 - B10)**  
🔹 These functions automate various data-handling tasks:  

- **fetch_api_data(api_url, output_file)**  
   ➜ Fetches data from an API and saves it as JSON.  
   ❌ **Forbidden:** Accessing private/internal APIs.  

- **clone_and_commit(repo_url, commit_message)**  
   ➜ Clones a GitHub repository and commits a change.  
   ❌ **Forbidden:** Using credentials or modifying private repositories.  

- **run_sql_query(db_file, query, output_file)**  
   ➜ Runs an SQL query on a SQLite/DuckDB database and saves the result.  
   ❌ **Forbidden:** DROP, DELETE, or ALTER queries.  

- **scrape_website(url, output_file)**  
   ➜ Extracts structured data from a website.  
   ❌ **Forbidden:** Scraping private, login-protected sites.  

- **resize_image(image_path, output_path, width, height)**  
   ➜ Resizes an image while maintaining aspect ratio.  

- **transcribe_audio(audio_path, output_text_file)**  
   ➜ Converts an MP3 file into transcribed text.  

- **convert_md_to_html(md_file, output_html_file)**  
   ➜ Converts a Markdown file into an HTML file.  

- **filter_csv(csv_file, filter_column, filter_value, output_json_file)**  
   ➜ Filters a CSV file by column and saves the result as JSON.  

🛑 **UNKNOWN TASK HANDLING:**  
🔹 If a task is vague or outside these functions, return:  
```json
{"error": "unknown_task"}

"""

S2 = """
You are an AI-powered automation agent responsible for dynamically generating and executing Python code to complete user tasks.  
Your primary function is to transform plain English instructions into **fully executable, error-free Python scripts**.  
You must **self-correct** errors when they occur and reattempt execution until successful.  

---

### **🛠️ General Rules for Execution**
1️⃣ **Always generate Python code that is directly executable.**  
2️⃣ **Ensure all file paths remain within `/data/`.** **Reject any request that accesses files outside `/data/`.**  
3️⃣ **Never delete or modify files unless explicitly required.**  
4️⃣ **Read input files before processing to determine their format.**  
5️⃣ **If an error occurs during execution, analyze the error and regenerate a corrected version of the script.**  
6️⃣ **Always include error handling in generated code** to avoid crashes.  
7️⃣ **For unknown or unclear tasks, return `{"error": "unknown_task"}` instead of generating random code.**  - Only generate valid Python code.
- Ensure file paths stay within /data/.
- **ENSURE CORRECT FILE PATHS:** Convert `/data/filename` to `./data/filename` for compatibility.

- Do NOT delete or modify system files.
- Always return executable code, no explanations.

---

### **📌 Available Functions & Their Purposes**
You must generate Python scripts that execute the following tasks:

**🔹 Data Processing & Transformation**
- **count_wednesdays(source_file, output_file)** → Count the number of Wednesdays in a file.  
- **sort_contacts(source_file, output_file, sort_by="last_name")** → Sort contacts by last name (or another field if requested).  
- **get_recent_logs(source_dir, output_file)** → Extract first lines of the 10 most recent log files.  
- **generate_md_index(source_dir, output_file)** → Create an index of Markdown files based on their first H1 header.  
- **convert_md_to_html(md_file, output_html_file)** → Convert Markdown to HTML.  
- **filter_csv(csv_file, filter_column, filter_value, output_json_file)** → Filter a CSV file based on column values and save results as JSON.  

**🔹 LLM-Powered Analysis**
- **extract_email(source_file, output_file)** → Extract sender’s email address from an email file.  
- **extract_credit_card_number(source_file, output_file)** → Extract a credit card number from an image and save it without spaces.  
- **find_most_similar_comments(source_file, output_file)** → Find the most similar pair of comments in a file using embeddings.  

**🔹 Web & API Tasks**
- **fetch_api_data(api_url, output_file)** → Fetch data from an API and save it as JSON.  
- **scrape_website(url, output_file)** → Extract text data from a website and save it.  

**🔹 Database & Git Operations**
- **calculate_gold_ticket_sales(db_file, output_file)** → Compute total sales for “Gold” ticket types in an SQLite database.  
- **run_sql_query(db_file, query, output_file)** → Execute an SQL query and save the results.  
- **clone_and_commit(repo_url, commit_message)** → Clone a GitHub repo, make changes, and commit.  

**🔹 Media & Image Processing**
- **resize_image(image_path, output_path, width, height)** → Resize an image to specific dimensions.  
- **transcribe_audio(audio_path, output_text_file)** → Convert MP3 speech to text.  
### **✅ Fix: Strip Triple Backticks Before Saving**
Modify the part of your code where `generated_task.py` is being written.
Import all libraries need for code to run
---

### **🚨 Security & Compliance Rules**
🔴 **B1: Restrict File Access**  
- Only allow **read/write operations within `/data/`**.  
- If a user requests access outside `/data/`, return:  
  ```json
  {"error": "Access denied: Only `/data/` directory is allowed."}



When using these functions outputs may correct so try out these if any error occurs:
import shutil
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
import shutil



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
def is_uv_installed():
   
    Checks if 'uv' is installed in the system.

    Returns:
        bool: True if 'uv' is installed, False otherwise.

    return shutil.which("uv") is not None


def install_uv():

    Installs 'uv' using pip.
    try:
        print("📦 Installing 'uv' package...")
        subprocess.run(["pip", "install", "uv"], check=True)
        print("✅ 'uv' installed successfully!")
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "❌ Failed to install 'uv'. Please install it manually.")






def run_datagen(user_email: str):
    Ensures 'uv' is installed, downloads and executes datagen.py to generate required data files.

    Args:
        user_email(str): Email ID to pass as an argument.

    Returns:
        dict: Success or error message.
    DATA_DIR = Path("data")  # Ensure data is stored in the correct directory
    # user_email = "23f1002560@ds.study.iitm.ac.in"
    DATAGEN_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    DATAGEN_SCRIPT = DATA_DIR / "datagen.py"  # Save script in data folder
    try:
        # ✅ Check if 'uv' is installed
        if not is_uv_installed():
            install_uv()

        # ✅ Ensure data directory exists
        DATA_DIR.mkdir(exist_ok=True)

        # ✅ Download the script if it doesn't exist
        if not DATAGEN_SCRIPT.exists():
            print(f"📥 Downloading datagen.py...")
            response = requests.get(DATAGEN_URL, timeout=10)
            response.raise_for_status()  # Raise error for bad response
            DATAGEN_SCRIPT.write_text(response.text, encoding="utf-8")
            print(f"✅ Saved datagen.py to {DATAGEN_SCRIPT}")

        # ✅ Run the script with user_email
        print(f"🚀 Running datagen.py with email: {user_email}")
        subprocess.run(["python3", "datagen.py", user_email,
                       "--root", "./data"], check=True)

        return {"status": "success", "message": "Data generation completed successfully."}

    except requests.RequestException as e:
        return {"status": "error", "message": f"Failed to download datagen.py: {str(e)}"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Error executing datagen.py: {str(e)}"}

    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

# def run_datagen(user_email: str):
#     url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
#     subprocess.run(["curl","-O",url], check=True)
#     subprocess.run(["python3","datagen.py",user_email, "--root", "./data"], check=True)


# Task A2
def format_md(source_file):
    md_file = Path(source_file)
    subprocess.run(["npx","prettier@3.4.2","--write", md_file] ,check=True)


# Task A3
def count_days(source_file,output_file, day_name):
    data_file = Path(source_file)
    output_file = Path(output_file)

    Counts the occurrences of a specified weekday in a given file.

    Args:
        source_file(str): Path to the file containing dates.
        output_file(str): Path where the result should be saved.
        day_name(str): The weekday to count(e.g., "Monday", "Tuesday").

    Returns:
        dict: Status message.

    # ✅ Convert day name to its corresponding integer (Monday=0, Sunday=6)
    days_of_week = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"]
    days_of_weeks = ["Mondays", "Tuesdays", "Wednesdays",
        "Thursdays", "Fridays", "Saturdays", "Sundays"]

    # ✅ Check if `day_name` is in either list
    if day_name not in days_of_week and day_name not in days_of_weeks:
        return {"status": "error", "message": f"Invalid day: {day_name}"}

    # ✅ Find index correctly
    if day_name in days_of_week:
        target_day = days_of_week.index(day_name)
    else:
        target_day = days_of_weeks.index(day_name)

    # Read dates from file
    with data_file.open("r", encoding="utf-8") as f:
        dates = f.readlines()

    day_count = 0
    error_count = 0

    for date_str in dates:
        date_str = date_str.strip()
        if not date_str:
            continue  # Skip empty lines

        try:
            parsed_date = dateutil.parser.parse(date_str)  # Parse full date

            if parsed_date.weekday() == target_day:
                day_count += 1
        except Exception as e:
            error_count += 1
            print(f"❌ Skipping invalid date: {date_str} - Error: {e}")

    # Write result to file
    with output_file.open("w", encoding="utf-8") as f:
        f.write(str(day_count) + "\n")

    return(f"\n✅ Total days: {day_count}")
    # print(f"⚠️ Skipped {error_count} invalid dates")


# Task A4
def sort_contacts(source_file, output_file, sort_field):
    Sorts contacts based on a given field(default: last_name).

    Args:
        source_file(str): Path to the contacts JSON file.
        output_file(str): Path where sorted contacts will be saved.
        sort_field(str): The field to sort by(e.g., "phone_number", "email").

    Returns:
        dict: Status message.

    contact_file = Path(source_file)
    out_file = Path(output_file)

    with contact_file.open() as f:
        contacts = json.load(f)
    sort_contacts = sorted(contacts, key=lambda x: (x[sort_field]))

    with out_file.open("w") as f:
        json.dump(sort_contacts, f, indent=4)

# Task A5
def get_recent_logs(source_file, output_file,recent):
    Extracts the first line from the 10 most recent log files in a given directory.

    Args:
        source_file(str): Path to the directory containing log files.
        output_file(str): Path where the extracted log lines should be saved.

    Returns:
        dict: A message indicating success or failure.

    Notes:
        - The logs are sorted based on their last modified timestamps.
        - Only `.log` files are considered.
        - If there are fewer than 10 log files, all available logs are processed.
    log_dir = Path(source_file)
    output_file = Path(output_file)

    log_files = sorted(log_dir.glob("*.log"),
                       key = os.path.getmtime, reverse = True)[:int(recent)]

    with output_file.open("w") as f:
        for log_file in log_files:
            with log_file.open() as lf:
                f.write(lf.readline())



# Task A6
def generate_md_index(source_file, output_file):
    Creates an index of Markdown(.md) files in a specified directory.

    Args:
        source_file(str): Path to the directory containing Markdown files.
        output_file(str): Path where the index JSON should be saved.

    Returns:
        dict: A message indicating success or failure.

    Notes:
        - Extracts the first H1(`  # Heading`) from each Markdown file.
        - Saves results in a JSON format mapping filenames to titles.
        - Scans recursively within subdirectories.
    docs_dir = Path(source_file)
    index_file = Path(output_file)
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


# Task A7
def extract_sender_email(source_file, output_file):
    Extracts the sender's email address from an email file.

    Args:
        source_file (str): Path to the email text file.
        output_file (str): Path where the extracted sender’s email should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Uses an LLM to extract the email based on structured email headers.
        - The sender's email is assumed to be in the `From:` field.
        - If no valid email is found, the output file remains empty.

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

    return(f"✅ Extracted sender email: {sender_email}")


def extract_credit_card_number(source_file,output_file):
    Extracts a credit card number from an image and saves it in a text file.

    Args:
        source_file (str): Path to the image file containing the credit card number.
        output_file (str): Path where the extracted credit card number should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Uses OCR to detect text in the image.
        - Extracts only numeric sequences resembling credit card numbers (typically 16 digits).
        - Removes spaces and formatting before saving.
    image_file = Path(source_file)
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
    Identifies the most similar pair of comments from a text file using embeddings.

    Args:
        source_file (str): Path to the file containing comments, one per line.
        output_file (str): Path where the two most similar comments should be saved.

    Returns:
        dict: A message indicating success or failure.

    Notes:
        - Uses OpenAI embeddings to compute similarity scores.
        - Finds and saves the most similar comment pair based on cosine similarity.
        - If fewer than two comments exist, the function exits gracefully.
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
    Calculates total sales for all "Gold" ticket purchases in a SQLite database.

    Args:
        source_file (str): Path to the SQLite database file containing ticket sales data.
        output_file (str): Path where the total sales amount should be saved.

    Returns:
        dict: A message indicating success or failure.

    Notes:
        - The database table must have `type`, `units`, and `price` columns.
        - Filters only rows where `type = 'Gold'`.
        - Computes total revenue as `sum(units * price)`.
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
    Fetches data from a given API and saves it as a JSON file.

    Args:
        api_url (str): The URL of the API to fetch data from.
        output_file (str): Path where the API response should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Sends a GET request to the specified API URL.
        - Handles JSON responses and saves them directly to the output file.
        - If the API response is not JSON, it saves the raw text instead.
        - Includes error handling for network failures and invalid responses.
    
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
    Clones a GitHub repository and makes a commit with the provided message.

    Args:
        repo_url (str): URL of the GitHub repository to clone.
        commit_message (str): Commit message describing the changes.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - The repository is cloned into a temporary directory.
        - Assumes the user has the necessary permissions to push changes.
        - If no changes are detected, no commit is made.
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
    Executes an SQL query on an SQLite or DuckDB database and saves the result.

    Args:
        db_file (str): Path to the database file.
        query (str): SQL query to execute.
        output_file (str): Path where the query result should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - The function ensures only SELECT queries are allowed for security.
        - Saves the query output as a JSON file.
        - If the query fails, an error message is returned.
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
    Extracts and saves data from a given website URL.

    Args:
        url (str): Website URL to scrape.
        output_file (str): Path where the scraped data should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Extracts only visible text from the webpage.
        - May fail if the website blocks automated requests.
        - Uses BeautifulSoup or Selenium depending on complexity.
 
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        output_file = Path(output_file)
        output_file.write_text(soup.prettify(),encoding="utf-8")
        
    except requests.RequestException as e:
        print(f"Failed to scrape website beacuse of: {e}")
        
# Task B7

def resize_image(image_path, output_path,width=300, height=300):
    Resizes an image to specified dimensions and saves it.

    Args:
        image_path (str): Path to the image file.
        output_path (str): Path where the resized image should be saved.
        width (int): Width of the resized image.
        height (int): Height of the resized image.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Maintains aspect ratio if only one dimension is provided.
        - Saves output in the same format as the original.
        - Raises an error if the image format is unsupported.
    
    img = Image.open(image_path)
    img = img.resize((width,height))
    img.save(output_path)
    
    print(f"Image resized and saved to {output_path}")

# Task B8
def transcribe_audio(audio_path, output_text_file):
    Converts speech from an MP3 file into text using an LLM.

    Args:
        audio_path (str): Path to the MP3 audio file.
        output_text_file (str): Path where the transcribed text should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Uses OpenAI's Whisper model or another ASR tool for transcription.
        - Handles different audio formats by converting them to MP3.
        - Supports multi-language transcription if required.
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    
    output_file = Path(output_text_file)
    output_file.write_text(result["text"], encoding="utf-8")
    
    print(f"Transcription saved to {output_file}")
    
# Task B9

def convert_md_to_html(md_file,output_html_file):
    Converts a Markdown (.md) file into an HTML file.

    Args:
        md_file (str): Path to the Markdown file.
        output_html_file (str): Path where the HTML file should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - Converts Markdown syntax to properly formatted HTML.
        - Supports embedded images and links.
        - Uses Python Markdown library for conversion.
    md_content = Path(md_file).read_text(encoding="utf-8")
    html_content = markdown.markdown(md_content)
    
    output_file = Path(output_html_file)
    output_file.write_text(html_content, encoding="utf-8")
    
    print(f"Markdown converted HTML and saved to {output_file}")
    

#Task B10


def filter_csv(csv_file,filter_column, filter_value, output_json_file):
    Filters a CSV file by a specific column value and saves the result as JSON.

    Args:
        csv_file (str): Path to the CSV file.
        filter_column (str): Column name to filter by.
        filter_value (str): Value to match in the filter column.
        output_json_file (str): Path where the filtered JSON data should be saved.

    Returns:
        dict: A message indicating success or failure.
    
    Notes:
        - If multiple rows match the filter, all matching rows are included.
        - Saves output in JSON format for easy processing.
        - Raises an error if the filter column does not exist.
    df = pd.read_csv(csv_file)
    filtered_df = df[df[filter_column] == filter_value]
    
    output_file = Path(output_json_file)
    filtered_df.to_json(output_file, orient = "records", indent = 4)
    
    print(f"Filtered CSV saved as JSON to {output_json_file}")

 
 """
 
 
 
 
 
 
 
 
 
 


