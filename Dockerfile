# -----------------------
# Stage 1: Build stage
# -----------------------
    FROM python:3.11-slim AS build-stage

    # Set environment variables
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    # Install build dependencies
    # (You may need build-essential if you're compiling some Python packages)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Copy and install Python dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # -----------------------
    # Stage 2: Final stage
    # -----------------------
    FROM python:3.11-slim
    
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # Install the system libraries needed by OpenCV
    RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*
    
    # Create a non-root user
    RUN useradd -m appuser
    USER appuser
    
    # Copy the Python site-packages and binaries from the build stage
    COPY --from=build-stage /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
    COPY --from=build-stage /usr/local/bin /usr/local/bin
    
    # Copy your app code
    COPY . .
    
    EXPOSE 8000
    
    HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:8000/health || exit 1
    
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    