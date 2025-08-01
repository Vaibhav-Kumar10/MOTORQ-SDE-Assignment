# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional for API only apps)
# RUN python manage.py collectstatic --noinput

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
