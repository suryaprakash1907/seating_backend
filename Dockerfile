# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the port Railway will assign
EXPOSE 8000

# Start Django with Railway PORT
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT}"]
