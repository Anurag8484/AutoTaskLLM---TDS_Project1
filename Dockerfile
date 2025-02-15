# Use an official Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Move inside /src (since code is there)
WORKDIR /app/src

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port 8000 for the API
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
