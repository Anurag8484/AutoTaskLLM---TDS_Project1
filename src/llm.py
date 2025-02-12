import os
import httpx
import requests
from pathlib import Path
from PIL import Image
import pytesseract
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
from dotenv import load_dotenv
import sqlite3


load_dotenv()

API_KEY = os.getenv("AIR_PROXY_TOKEN")

chat_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}



### A7, Extracting sender's email:
Data_dir = Path(__file__).parent / "data"
def extract_email():
    
    email_file = Data_dir / "email.txt"
    output_file = Data_dir / "sender-email.txt"
    with email_file.open("r",encoding="utf-8") as f:
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




def extract_card_number():
    image_file = Data_dir / "credit_card.png"
    output_file = Data_dir / "credit_card.txt"
    
    image = Image.open(image_file)
    extracted_text = pytesseract.image_to_string(image)
    
    
    # cleaned_card_number = "".join(filter(str.isdigit(),extracted_text))
    cleaned_card_number = "".join(c for c in extracted_text if c.isdigit())[:12]
    with output_file.open("w", encoding="utf-8") as f:
        f.write(cleaned_card_number + "\n")
        
    print(f"✅ Extracted Credit Card Number: {cleaned_card_number}")




def find_most_similar_comments():
    comments_file = Data_dir / "comments.txt"
    output_file = Data_dir / "comments-similar.txt"
    
    with comments_file.open("r",encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]
        


    embedding_response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/embeddings",
        headers=headers,
        json = {
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

    embeddings = np.array([item["embedding"] for item in embedding_response.json()["data"]])
       
    similarity_matrix = cosine_similarity(embeddings)
    
    np.fill_diagonal(similarity_matrix,-1)
    
    i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    
    with output_file.open("w", encoding="utf-8") as f:
        f.write(comments[i] + "\n" + comments[j] + "\n")
    print(f"✅ Most Similar comments saved to {output_file}")
    



def calculate_gold_tickets_sales():
    
    DB_FILE = Data_dir / "ticket-sales.db"
    OUTPUT_FILE = Data_dir / "ticket-sales-gold.db"
    
    if not DB_FILE.exists():
        print("DB file not found")
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0]
        
        
        total_sales = total_sales if total_sales is not None else 0
        
        
        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            f.write(str(total_sales)+ "\n")
            
        print(f"Total 'Gold' ticket sales are: {total_sales}")
        
    except sqlite3.Error as e:
        print(f"Database Error{e}")
    finally:
        conn.close()
        

    