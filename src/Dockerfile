# Using the slim-bullseye image
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt .

#install python dependencies
RUN pip install -r requirements.txt

# Expose the Hypercorn port
EXPOSE 8000

#copy all the django project
COPY . .

#execute the commands inside the entrypoint.sh
# ENTRYPOINT [ "sh", "./entrypoint.sh" ]