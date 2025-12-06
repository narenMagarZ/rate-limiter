# ---------- Stage 1: Builder ----------
  FROM python:3.13-slim AS builder

  WORKDIR /app
  
  # Install build dependencies only for this stage (not included in final image)
  RUN apt-get update && apt-get install -y --no-install-recommends build-essential
  
  COPY requirements.txt .
  RUN pip install --user --no-cache-dir -r requirements.txt
  
  
  # ---------- Stage 2: Final ----------
  FROM python:3.13-slim
  
  WORKDIR /app
  
  # Install curl for healthcheck (very lightweight)
  RUN apt-get update && apt-get install -y --no-install-recommends curl && \
      rm -rf /var/lib/apt/lists/*
  
  # Copy installed Python packages from builder layer
  COPY --from=builder /root/.local /root/.local
  ENV PATH="/root/.local/bin:${PATH}"
  
  # Copy application code
  COPY . .
  
  EXPOSE 8000
  
  HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/api/public/v1/health || exit 1
  
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  