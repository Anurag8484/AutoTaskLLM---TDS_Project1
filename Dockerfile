# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ARG AIPROXY_TOKEN
ENV AIPROXY_TOKEN=$AIPROXY_TOKEN
ENV PYTHONPATH="/app"

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (Tesseract, Node.js, npm)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    curl \
    nodejs \
    npm \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Copy the project files
COPY . /app

# Install dependencies using UV from pyproject.toml
RUN uv venv .venv && uv pip install --system .

# Install Prettier globally using npm
RUN npm install -g prettier@3.4.2

# Expose port 8000 for the API
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
