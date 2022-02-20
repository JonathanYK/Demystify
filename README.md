# Sessions project


The main purpose of this project is managing sessions with Flask framework using a SQLite database (using SQLAlchemy as ORM).
There are 2 main APIs that has to be handled, according to the assignment:


>1. Generating a  session id (defined as random number with exact 9 digits), then adding it to db.
>2. Recieves a session id and a json file, saving the relevant fields as a log (using both stream_handler and file_handlers - printing the log to a console/dedicated file) and saves the message of the session id to the db.

Supported routes splitted to blueprints, 2 configuration files under `//src/instance` defined in order to execute this project both on test and production environments.
Make sure to edit `//src/instance/key.txt` file with a random new key.
In order to ensure that the access to db is thread safe - scoped_session of SQLAlchemy is used.

The project has both unit and functionality tests, designed using Pytest framework.

This project has a dockerfile in order to be executed on containers.
In order to run this project on a container, you can use the following commands as example:  
`docker build -t sessions_proj_img .`  
`docker run -p 8081:5000 sessions_proj_img`
  
  
`IDE: Visual Studio Code v1.64.2`
