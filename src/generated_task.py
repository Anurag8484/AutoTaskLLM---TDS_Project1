import shutil
import subprocess
import requests
from pathlib import Path

def is_uv_installed():
    return shutil.which("uv") is not None

def install_uv():
    try:
        print("📦 Installing 'uv' package...")
        subprocess.run(["pip", "install", "uv"], check=True)
        print("✅ 'uv' installed successfully!")
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ Failed to install 'uv'. Please install it manually.")

def run_datagen(user_email: str):
    DATA_DIR = Path("./data")  # Ensure data is stored in the correct directory
    DATAGEN_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    DATAGEN_SCRIPT = DATA_DIR / "datagen.py"  # Save script in data folder
    try:
        # Check if 'uv' is installed
        if not is_uv_installed():
            install_uv()

        # Ensure data directory exists
        DATA_DIR.mkdir(exist_ok=True)

        # Download the script if it doesn't exist
        if not DATAGEN_SCRIPT.exists():
            print(f"📥 Downloading datagen.py...")
            response = requests.get(DATAGEN_URL, timeout=10)
            response.raise_for_status()  # Raise error for bad response
            DATAGEN_SCRIPT.write_text(response.text, encoding="utf-8")
            print(f"✅ Saved datagen.py to {DATAGEN_SCRIPT}")

        # Run the script with user_email
        print(f"🚀 Running datagen.py with email: {user_email}")
        subprocess.run(["python3", str(DATAGEN_SCRIPT), user_email, "--root", "./data"], check=True)

        return {"status": "success", "message": "Data generation completed successfully."}

    except requests.RequestException as e:
        return {"status": "error", "message": f"Failed to download datagen.py: {str(e)}"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Error executing datagen.py: {str(e)}"}

    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

# Run the data generation script
result = run_datagen("23f1002560@ds.study.iitm.ac.in")
print(result)