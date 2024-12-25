# Base stage
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \  
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Development stage
FROM base AS development

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set development environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV ENVIRONMENT=development
ENV PYTHONUNBUFFERED=1

# The command to run the application with hot reloading
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base AS production

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set production environment variables
ENV PORT=8080
ENV HOST=0.0.0.0
ENV ENVIRONMENT=production
# Ensures Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1  

# Create a non-root user
RUN adduser --system --group app
RUN chown -R app:app /app
USER app

# Healthcheck to verify the application is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# The command to run the application
# Note the removal of the --reload flag and the addition of --log-level=info
CMD exec uvicorn app.main:app \
    --host ${HOST} \
    --port ${PORT:-8000} \
    --workers 1 \
    --timeout-keep-alive 75 \
    --log-level info