# Use the Python 3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the contents of the "opt" directory from the host to the container's current directory
ADD ["opt", "./opt"]

# Install dependencies for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y curl
RUN apt-get install -y libgomp1

# Install Python dependencies from the optional_requirement.txt file
RUN pip install -r opt/optional_requirement.txt

# Copy the contents of the "models," "scripts," and "data" directories from the host to the container's corresponding directories
ADD ["models", "./models"]
ADD ["scripts", "./scripts"]
ADD ["data", "./data"]

# Expose port 9696 for incoming network connections
EXPOSE 9696

# Set the entry point for the container, which runs the Gunicorn web server to serve the predict.py application on port 9696
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app", "--chdir", "./scripts/"]
