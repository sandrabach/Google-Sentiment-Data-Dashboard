# Use an official Python runtime as the parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Expose the port that the Flask app will listen on
EXPOSE 8080

# Command to run the Flask application when the container starts
CMD ["python", "main.py"]