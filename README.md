# Session project

The objective of this project is to manage sessions using the Flask framework and a SQLite database with SQLAlchemy as the ORM. 

The assignment requires the handling of two main APIs:
1. Generating a session ID, defined as a random number with exactly 9 digits, and adding it to the database.
2. Receiving a session ID and a JSON file, saving relevant fields as a log using both stream_handler and file_handlers, printing the log to a console or dedicated file, and saving the message of the session ID to the database.

The supported routes are split into blueprints, and there are two configuration files located in `/src/instance` to facilitate the execution of the project in both test and production environments. It is important to note that the `/src/instance/key.txt` file must be edited with a new, randomly generated key. Additionally, to ensure thread-safe access to the database, the `scoped_session` of SQLAlchemy is utilized. The project includes both unit and functionality tests that were designed using the Pytest framework.

The project contains a Dockerfile that allows it to be executed within a container. To run the project in a container, the following example commands can be used:

`docker build -t sessions_proj_img .`

`docker run -p 8081:5000 sessions_proj_img`


## CD overview
 
The project includes a docker-compose.yml file with support for nginx. To build the project using the docker-compose file, execute the following command:
`docker-compose up --build -d`

The Terraform code located in `/src/tf/main.tf` creates an AWS environment with all of the required resources as previewed below.

Upon each push to the main branch, there are two GitHub actions triggered. The first action builds and pushes the Docker image to Docker Hub. The second action triggers Pytest to run the tests and provide the test results at the end of the push.

There is a crontab configuration that runs once per day and restarts the docker-compose. The configuration is explained in `/reclone_project_and_docker_compose.sh` and follows these steps:

1. Compose down the active containers (flask_app and nginx).
2. Clone the project from the GitHub repository (current repo).
3. Restart the compose with the latest code and image from Docker Hub, which was uploaded by the GitHub action explained above.

## Terraform Cloud Environment Visualization

![image](https://github.com/JonathanYK/Sessions_Project/blob/main/src/tf/Terraform_Visualization.png)

