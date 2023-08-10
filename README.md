

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

You need to put in the env files that are present in the project, the values that you have, so:
* In the PostgreSQL credentials, put your credentials;
* In SECRET_KEY, put your secret key you have when you create the Django project;
* In DEBUG put False when you want to put in production or True when you are developing your application;
* In DJANGO_ALLOWED_HOSTS, put the hosts you want to allow to use your application, for example: "localhost,127.0.0.1"
* In RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY put the public and private keys you get when you create your captcha key at this site: https://www.google.com/recaptcha/admin/create

Also put the email host password and your email address in the .env file; to do that, you need to follow these steps:

* Go to https://myaccount.google.com/
* Click on security;
* Search for app password on search filter bar;
* Click on Other in Select app and give it a name;
* Save the password;
* Paste it into the EMAIL_HOST_PASSWORD field in env file and put in EMAIL_FROM the email address you want to use to send the emails;


And that's it, hope you like it!
