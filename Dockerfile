# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
