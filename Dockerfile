# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# and the gcc compiler and other dependencies for hdbscan
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libpython3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc g++ libpython3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]

