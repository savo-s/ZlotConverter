FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/data


COPY requirements.txt* ./
# Install dependencies
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
    python-dotenv \
    pydantic_settings

# Copy application files
COPY . .

EXPOSE 8000

# Hot reload command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]