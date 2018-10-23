# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory to /app
WORKDIR /templates_service

# Copy the current directory contents into the container at /app
COPY . /templates_service

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 8000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["nameko", "run", "templates_service", "--broker", "amqp://guest:guest@localhost"]
