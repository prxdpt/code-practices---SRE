# ────────────────────────────────
#  BUILD STAGE
# ────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip + install poetry or use requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy dependency files first (better caching)
COPY pyproject.toml poetry.lock requirements.txt* ./

# If you use poetry (recommended for modern projects)
# RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --only main
# If you use requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Optional: run tests / lint in build stage
# RUN pytest || true

# ────────────────────────────────
#  RUNTIME STAGE (very small)
# ────────────────────────────────
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (mainly for documentation)
EXPOSE 8000

# Health endpoint should exist in your app
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

# Default command will be overridden in docker-compose
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]