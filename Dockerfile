# No1
# FROM python:3.10-alpine

# # Set environment variables
# ENV PYTHONUNBUFFERED=1
# ENV SENTRY_DSN="${LIVEARTCORNER_SENTRY_DSN}"

# # Set the working directory
# WORKDIR /app


# # Copy the requirements file to the working directory
# COPY requirements.txt /app/

# COPY ./manage.py .


# # Install dependencies
# #RUN pip install --no-cache-dir -r requirements.txt


# # Copy the rest of the application code to the working directory
# COPY . .

# # Collect static files
# COPY staticfiles /app/staticfiles

# RUN chmod -R 755 /app/staticfiles

# RUN chmod -R 777 /app/media

# # Command to run the application with Gunicorn
# CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug


# Use the official Python image from the Docker Hub
# FROM python:3.10-alpine

# # Set environment variables
# ENV PYTHONUNBUFFERED=1
# ENV SENTRY_DSN="${LIVEARTCORNER_SENTRY_DSN}"

# # Set the working directory
# WORKDIR /app

# # Install system dependencies
# RUN apk update && apk add --no-cache musl-dev gcc g++ libffi-dev openssl-dev

# # Copy the requirements file to the working directory
# COPY requirements.txt /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Install spaCy model
# RUN pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl#sha256=86cc141f63942d4b2c5fcee06630fd6f904788d2f0ab005cce45aadb8fb73889

# # Copy the rest of the application code to the working directory
# COPY . /app

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Set permissions for static and media files
# RUN chmod -R 755 /app/staticfiles && chmod -R 777 /app/media

# # Command to run the application with Gunicorn
# CMD ["gunicorn", "liveartcorner.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "300", "--log-level", "debug"]


# Start with a Python Alpine image
# Start with a Python image (non-Alpine)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download and install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code
COPY . /app/

# Copy static files
COPY staticfiles /app/staticfiles
RUN chmod -R 755 /app/staticfiles

# Ensure media directory has the right permissions
RUN chmod -R 777 /app/media

# Start your application
#CMD ["python", "app.py"]
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug

