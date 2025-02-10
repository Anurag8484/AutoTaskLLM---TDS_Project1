AutoTaskLLM - LLM-Based Automation Agent
🚀 AutoTaskLLM is an automation agent that executes multi-step tasks using a Large Language Model (GPT-4o-Mini). It parses natural language instructions and performs deterministic operations, making it a powerful tool for CI/CD pipelines and business automation.

📌 Features
✅ Accepts plain-English tasks and executes them via an API
✅ Uses GPT-4o-Mini to interpret task descriptions
✅ Supports multi-step processing for various operations
✅ Provides file content verification via a GET endpoint
✅ Ensures security constraints: No data exfiltration or deletion
✅ Containerized with Docker for easy deployment

⚙️ Installation

1. Clone the Repository
bash
Copy
Edit
git clone <https://github.com/your-username/AutoTaskLLM.git>
cd AutoTaskLLM
2. Set Up Virtual Environment (Using UV)
bash
Copy
Edit
uv venv .  
source .venv/bin/activate  
3. Install Dependencies
bash
Copy
Edit
uv pip install -r requirements.txt
4. Set Up API Token (GPT-4o-Mini)
Create a .env file in the root directory:

ini
Copy
Edit
AIPROXY_TOKEN=your_openai_api_key
🚀 Running the Application
Using Python (Development Mode)
bash
Copy
Edit
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
Using Docker (Production Mode)
bash
Copy
Edit
docker build -t autotaskllm .
docker run -e AIPROXY_TOKEN=your_openai_api_key -p 8000:8000 autotaskllm
🛠️ API Endpoints
1️⃣ Run a Task
http
Copy
Edit
POST /run?task=<task_description>
Executes a task based on natural language input
Uses LLM to interpret the instruction
Returns 200 OK on success, 400 Bad Request for invalid tasks
2️⃣ Read a File
http
Copy
Edit
GET /read?path=<file_path>
Returns file contents for verification
Returns 404 Not Found if the file doesn’t exist
📂 Project Structure
bash
Copy
Edit
AutoTaskLLM/
│── data/                    # Stores generated & processed files
│── src/                     # Source code
│   ├── api.py               # FastAPI endpoints
│   ├── task_handler.py       # Handles task execution
│   ├── llm_agent.py          # Calls the LLM for parsing
│   ├── utils.py              # Utility functions
│── .env                      # API tokens (not committed)
│── requirements.txt          # Dependencies
│── Dockerfile                # Containerization
│── README.md                 # Documentation
│── LICENSE                   # MIT License
📖 Supported Tasks
Phase A: Operations Tasks
✅ Formatting files using Prettier
✅ Sorting JSON arrays
✅ Extracting & processing logs
✅ Counting specific occurrences in text files
✅ Running SQL queries on SQLite

Phase B: Business Tasks
✅ Fetching & storing API data
✅ Git repository automation
✅ SQL & DuckDB queries
✅ Web scraping
✅ Image compression & OCR
✅ Audio transcription & Markdown conversion

🛠️ Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a new branch (feature/your-feature)
Commit changes (git commit -m "Added feature")
Push to your branch (git push origin feature/your-feature)
Create a Pull Request
