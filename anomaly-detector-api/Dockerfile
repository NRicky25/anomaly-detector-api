# Dockerfile

# Stage 1: Build the Python environment and install dependencies
FROM python:3.11-slim-bullseye AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# This allows Docker to cache the dependency installation if requirements.txt doesn't change
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final production image
# Use the same slim base image
FROM python:3.11-slim-bullseye

# Set the working directory in the final image
WORKDIR /app

# Copy only the installed dependencies from the 'builder' stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy your application code and your ML model into the container
COPY app ./app

# NEW LINE HERE: Copy your ML model directory into the container
COPY model ./model

# Expose the port that your FastAPI application will run on
EXPOSE 8000

# Define the command to run your FastAPI application when the container starts
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]