# Use the Python 3.9-slim as the base image
FROM python:3.9-slim

# Install pipenv library in Docker 
RUN pip install pipenv


# Set the working directory inside the container to /app
WORKDIR /app


# Copy the Pip files into our working derectory 
COPY ["Pipfile", "Pipfile.lock", "./"]

# install the pipenv dependencies for the project and deploy them.
RUN pipenv install --deploy --system


# Install dependencies for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y curl
RUN apt-get install -y libgomp1

# Copy the contents of the "models," "scripts," and "data" directories from the host to the container's corresponding directories
ADD ["models", "./models"]
ADD ["scripts", "./scripts"]
ADD ["data", "./data"]

# Expose port 9696 for incoming network connections
EXPOSE 9696

# Set the entry point for the container, which runs the Gunicorn web server to serve the predict.py application on port 9696
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app", "--chdir", "./scripts/"]
