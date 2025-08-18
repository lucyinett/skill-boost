# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /skill-boost-recommendation-system
WORKDIR /skill-boost-recommendation-system

# Copy the current directory contents into the container at /skill-boost-recommendation-system
COPY . /skill-boost-recommendation-system

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Ensure Python will look in the correct directory for your modules
ENV PYTHONPATH=/skill-boost-recommendation-system

# Run the app when the container launches specifying the module path
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
