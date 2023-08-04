

# Introduction

The goal of this project is to create a web application where users can register, login and create an event that will be shown in the calendar event. The user that creates the event will have the ability to edit them and the ones that are not the editors of the event will have the ability to participate to them or opt out if they have already participate.


## Technologies used
I decided to simulate a "production" mode, using: 
* Docker; 
* PostgreSQL as the default database;
* Nginx as the web server, to handle the static files and that works as a reverse proxy;
* Hypercorn as the ASGI web server that makes the django project go up and running.



# Usage

To use this project you need to:

### Run Docker 

There are a few steps needed to run the project: 

    docker-compose build

This command will build or rebuilds images in the docker-compose.yml file that contains all the Dockerfile that will automatically creates containers on the Docker platform.

Then you need to run the following command:

    docker-compose up

This command will start and run an entire application on a standalone host that contains multiple services like django, nginx and db.

Another useful command is:

    docker-compose down -v

This will stop and remove containers, volumes, networks and images created by the "docker-compose up" command.

You can also run this command:

    docker-compose up --build

This will run both the build and the up docker commands.
    

# A Few Other Things 

I decided to leave the .env file and don't put it the gitignore, in this way you can run and test the application with the postgres credentials.

The email to confirm right now will be sent to my email address, so if you want to test this, you will obviously have to change these credentials (But I know that you already know that better than me :smile: ).


There are some bugs, I recently solved the one related to the email (now it also changes the name of the event owner when he changes his email), but if you find any bugs, let me know!

And that's it, hope you like it!
