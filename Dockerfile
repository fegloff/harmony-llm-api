	# Use the official Python 3.11 image as the base image
FROM python:3.10.13
 
# Set environment variables for configuration
ENV FLASK_APP=main.py
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/res/service_account.json
 
# Set default values for environment variables
ENV FLASK_ENV=production
 
# Set the working directory inside the container
WORKDIR /app

# Mount the volume to /app/data
VOLUME ["/app/data"]
 
# Copy the project files to the working directory
COPY . /app

RUN apt-get update && apt-get install -y \
    libgeos-dev
# Install the project dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 
# Expose the port on which the Flask app will run
EXPOSE 8080
 
# Run the Flask app when the container starts
# CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0"]
CMD ["python", "main.py"]

