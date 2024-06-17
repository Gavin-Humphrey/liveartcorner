# FROM python:3.10-alpine

# # Set environment variables
# ENV PYTHONUNBUFFERED=1

# # Set the working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code to the working directory
# COPY . /app/

# # Collect static files
# RUN python manage.py collectstatic --noinput

# # Run migrations
# RUN python manage.py migrate

# # Command to run the application
# #CMD ["gunicorn", "liveartcorner.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug


FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Command to run the application with Gunicorn
#CMD ["gunicorn", "liveartcorner.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD gunicorn liveartcorner.wsgi:application --bind 0.0.0.0:${PORT} --timeout 300 --log-level debug
