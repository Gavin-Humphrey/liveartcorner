# Use Python 3.10 Alpine image as the base image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SENTRY_DSN="${LIVEARTCORNER_SENTRY_DSN}"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Copy the manage.py script to the working directory
COPY ./manage.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the working directory
COPY . /app/

# Create a directory for static files in the container


# Command to run the application using Gunicorn
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug

