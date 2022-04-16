# Session project


The main purpose of this project is managing sessions with Flask framework using a SQLite database (using SQLAlchemy as ORM).
There are 2 main APIs that has to be handled, according to the assignment:


>1. Generating a  session id (defined as random number with exact 9 digits), then adding it to db.
>2. Receiving a session id and a json file, saving the relevant fields as a log (using both stream_handler and file_handlers - printing the log to a console/dedicated file) and saves the message of the session id to the db.

Supported routes splitted to blueprints, 2 configuration files under `/src/instance` defined in order to execute this project both on test and production environments.
Make sure to edit `/src/instance/key.txt` file with a random new key.
In order to ensure that the access to db is thread safe - scoped_session of SQLAlchemy is used.

The project has both unit and functionality tests, designed using Pytest framework.

This project has a dockerfile in order to be executed on containers.
In order to run this project on a container, you can use the following commands as example:  
`docker build -t sessions_proj_img .`  
`docker run -p 8081:5000 sessions_proj_img`
  

## CD overview

There is a docker-compose.yml with nginx support.  
In order to build using the docker compose file, use the command:  
`docker-compose up --build -d`  
  
The terraform code located in `/src/main.tf` creates aws environment with all required resources.

On each push to the main branch, there is a github action that builds and pushs the docker image to docker hub

Once on each day, there is crontab configuration (explained in `/reclone_project_and_docker_compose.sh`) that restarting the docker-compose:
>1. Composing down the active containers (flask_app and nginx).
>2. Cloning the project from github repo (current repo).
>3. Restart the compose with the latest image from docker hub uploaded by github action explained above.

## Env preview

![image](https://user-images.githubusercontent.com/48648513/162792774-fbfdb2ff-4681-49d2-b8fe-4ff77f3c8109.png)


  


`Python version: 3.8.10`  
`Flask version: >=2.0.2`  
`Docker compose version: 3`  
`Terraform version: ~> 4.6.0`  
`IDE: Visual Studio Code v1.64.2`  

