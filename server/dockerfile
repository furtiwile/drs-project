# Use a more stable Python version
FROM python:3.14.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development

# Create a non-root user
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Switch to non-root user
USER flaskuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]