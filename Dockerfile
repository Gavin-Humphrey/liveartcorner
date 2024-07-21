FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --progress-bar off --no-build-isolation -r requirements.txt

# Download and install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code
COPY . /app/

# Copy static files
COPY staticfiles /app/staticfiles
RUN chmod -R 755 /app/staticfiles

# Ensure media directory has the right permissions
RUN mkdir -p /app/media && chmod -R 777 /app/media

# Expose the port your app runs on
EXPOSE ${PORT}

# Command to run the application with Gunicorn
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
