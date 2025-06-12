# Dockerfile

FROM python:3.12.3-slim

ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Django's default port
EXPOSE 8000

# Start gunicorn
# CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "3", "--timeout", "600"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

