import os
import httpx
import requests
from pathlib import Path
from PIL import Image
import pytesseract
import numpy as np
from dotenv import load_dotenv


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
