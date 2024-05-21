# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libhdf5-serial-dev \
    hdf5-tools

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install -r requirements.txt

# Make the port available to the world outside this container
# (This line is optional and primarily used for local development; Heroku sets the PORT environment variable)
EXPOSE 8000

# Run command to start Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT Riddle_Me_This.wsgi"]
