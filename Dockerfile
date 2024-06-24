FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SENTRY_DSN="${LIVEARTCORNER_SENTRY_DSN}"

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

COPY ./manage.py .


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Collect static files
COPY staticfiles /app/staticfiles

RUN chmod -R 755 /app/staticfiles

RUN chmod -R 777 /app/media

# Command to run the application with Gunicorn
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug