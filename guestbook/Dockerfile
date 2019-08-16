# Base the image off of the Ubuntu 18.04 image from Dockerhub
FROM ubuntu:18.04

# Set the Maintainer label to your name.
LABEL maintainer="Chase Hennion"

# Install python3 and python3-pip via apt
RUN apt-get update \
  && apt-get install -y python3 python3-pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists*

# Install flask, flask-wtf and redis via pip3
RUN pip3 install flask flask-wtf redis

# Create the flask directory /app
RUN mkdir /app

# Copy in the flask application in ./app into /app in the image.
COPY app /app

# Set /app as the working directory
WORKDIR /app

# Set the LC_ALL environment variable to C.UTF-8.
ENV LC_ALL=C.UTF-8

# Set the LANG environment variable to C.UTF-8.
ENV LANG=C.UTF-8

# Set the FLASK_APP environment variable to guestbook.py
ENV FLASK_APP=guestbook.py

# Expose port 5000 for Flask.
EXPOSE 5000

# Set the entrypoint to python3 -m flask
ENTRYPOINT [ "python3", "-m", "flask" ]

# Set the command to run run and be sure to include the option --host=0.0.0.0
CMD [ "run", "--host=0.0.0.0" ]