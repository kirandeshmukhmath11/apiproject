FROM django 
FROM python:3.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /api_docker

# Set the working directory to /music_service
WORKDIR /api_docker

# Copy the current directory contents into the container at /music_service
COPY . /api_docker/
#ADD . /music_service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
RUN ls -a
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]