# Lean production serving image based on python:3.11-slim
FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install only lean serving runtime dependencies (no MLflow, no pytest)
COPY requirements-serve.txt .
RUN pip install --no-cache-dir -r requirements-serve.txt

# Copy serialized model, FastAPI app, and web UI
COPY model/ model/
COPY static/ static/
COPY app.py .

# Create logs directory for drift logging
RUN mkdir -p logs

# Expose FastAPI port
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
