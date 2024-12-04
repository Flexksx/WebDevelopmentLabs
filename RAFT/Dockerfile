# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the node script into the container
COPY node.py .

# Expose the port
EXPOSE 5000-5010

# Command to run the node
CMD ["python", "node.py"]
