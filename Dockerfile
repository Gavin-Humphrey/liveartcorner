FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SENTRY_DSN="${LIVEARTCORNER_SENTRY_DSN}"

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
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Download and install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code
COPY . /app/

# Copy static files and set permissions
COPY staticfiles /app/staticfiles
RUN chmod -R 755 /app/staticfiles

# Ensure media directory has the right permissions
RUN chmod -R 777 /app/media

# Start your application
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
