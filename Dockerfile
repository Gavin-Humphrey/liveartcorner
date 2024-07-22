FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apk update \
    && apk add --no-cache \
       build-base \
       libffi-dev \
       openssl-dev \
    && rm -rf /var/cache/apk/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

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