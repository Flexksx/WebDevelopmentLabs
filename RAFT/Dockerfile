# Use a lightweight Python image
FROM python:3.12-slim

# Set a working directory in the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install any Python dependencies.
# If you have a requirements.txt or pyproject.toml, use that.
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port you are binding to (e.g., 5000)
EXPOSE 5000

# Set an environment variable for the IP and port if needed
ENV RAFT_ADDRESS=0.0.0.0
ENV RAFT_PORT=5000
ENV PYTHONUNBUFFERED=1

# The default command will run your main node program
CMD ["python", "main.py"]
