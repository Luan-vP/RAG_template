# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app files to the working directory
COPY src/ .

# Expose the port on which the app will run
EXPOSE 8888

ENV WEAVIATE_HOST=host.docker.internal

# Start the FastAPI app
CMD ["uvicorn", "rag_router.server:app", "--host", "0.0.0.0", "--port", "8888"]