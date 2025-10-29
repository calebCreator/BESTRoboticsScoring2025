FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY src/ /app/

EXPOSE 5000

# Use gunicorn for production-like runs. Falls back to the Flask dev server
# if you prefer to run `python main.py` instead (uncomment the CMD below).
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app", "--workers", "1", "--threads", "4"]
# CMD ["python", "main.py"]
