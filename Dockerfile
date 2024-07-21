FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and other dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt before the rest of the application
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --disable-pip-version-check setuptools wheel \
    && pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Download the spaCy model wheel file
RUN curl -L -o en_core_web_sm-3.7.1-py3-none-any.whl https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Install the spaCy model wheel file
RUN pip install en_core_web_sm-3.7.1-py3-none-any.whl \
    && python -m spacy link en_core_web_sm en

# Copy the rest of your application code
COPY . /app/

# Ensure media directory has the right permissions
RUN mkdir -p /app/media && chmod -R 777 /app/media

# Expose the port your app runs on
EXPOSE ${PORT}

# Command to run the application with Gunicorn
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
