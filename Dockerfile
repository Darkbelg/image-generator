# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create output directory for images
RUN mkdir -p output

# Expose the default Gradio port
EXPOSE 7860

# Set environment variable for Gradio to be accessible from outside container
ENV GRADIO_SERVER_NAME=0.0.0.0

# Command to run the application
CMD ["python", "app.py"]
