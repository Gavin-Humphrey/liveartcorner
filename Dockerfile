FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt before the rest of the application
COPY requirements.txt /app/

# Install Python dependencies without upgrading pip
RUN pip install --no-cache-dir --disable-pip-version-check setuptools wheel \
    && pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Install spaCy model separately
RUN python -m spacy download en_core_web_sm

# Copy the rest of your application code
COPY . /app/

# Ensure media directory has the right permissions
RUN mkdir -p /app/media && chmod -R 777 /app/media

# Expose the port your app runs on
EXPOSE ${PORT}

# Command to run the application with Gunicorn
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
