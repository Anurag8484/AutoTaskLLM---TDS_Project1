# Use an official Python base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AIPROXY_TOKEN=${AIPROXY_TOKEN}

# Set the working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install essential system packages and dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    tesseract-ocr \
    libtesseract-dev \
    ffmpeg \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
