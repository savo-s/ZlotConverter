FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Create data directory
RUN mkdir -p /app/data

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    fastapi-users[sqlalchemy] \
    sqlmodel \
    aiosqlite \
    requests \
    apscheduler \
    python-jose[cryptography] \
    passlib[bcrypt] \
    uvicorn \
    python-dotenv

# Set environment variables
ENV SECRET=your_strong_secret_key_here

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]