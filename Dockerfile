
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-tk \
    tk-dev \
    x11-apps \
    xvfb \
    && rm -rf /var/lib/apt/lists/*



# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code from the host to the container at /app
COPY . .
COPY src/ /app/src/
EXPOSE 5000

# Run the application
CMD ["xvfb-run","python", "./src/main.py"]
