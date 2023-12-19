# Use a slim version of Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Run the Flask application using Gunicorn on port 80 by default (or use PORT env var if set)
CMD ["sh", "-c", "gunicorn -b :${PORT:-80} src/app:app"]
