# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY . .

# Expose the port Flask runs on
EXPOSE 10000

# Run the application
CMD ["python", "app.py"]
