FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for psycopg2 and FAISS
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN sed -i 's/\r$//' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
