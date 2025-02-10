import requests
import sys
import subprocess

def run_datagen(user_email: str):
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    script_path = "datagen.py"

    response = requests.get(url)
    if response.status_code == 200:
        with open(script_path, "w") as f:
            f.write(response.text)
        print("✅ datagen.py downloaded successfully.")
    else:
        print("❌ Failed to download datagen.py")
        print(response)
        sys.exit(1)
    
    subprocess.run(["uv","python", script_path,user_email], check=True)
    print(f"✅ datagen.py executed with email {user_email}")
    
if __name__ == "__main__":
    user_email = "23f1002560@ds.study.iitm.ac.in"
    run_datagen(user_email)
