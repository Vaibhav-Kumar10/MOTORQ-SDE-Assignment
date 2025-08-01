FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app code
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Set env vars
ENV DJANGO_SETTINGS_MODULE=oj.settings
ENV PYTHONUNBUFFERED=1

# Run migrations and start Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]
