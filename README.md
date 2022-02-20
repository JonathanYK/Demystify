# Demystify project

IDE: Visual Studio Code v1.64.2

The main purpose of this project is managing sessions using Flask framework in front of an SQLite database (using SQLAlchemy as ORM).
There are 2 main APIs that has to be handled, according to the assignment:


`1. Generating a  session id (defined as random number with exact 9 digits), then adding it to db.`
`2. Recieves a session id and a json file, saving the relevant fields as a log (using both stream_handler and file_handlers - printing the log to a console/dedicated file) and` `saves the message of the session id to the db.`

Supported routes splitted to blueprints, 2 configurations defined in order to execute this project both on test and production environments.
In order to ensure that the access to db is thread safe - scoped_session of SQLAlchemy is used.

The project has both unit and functionality tests, designed using Pytest framework.

This project has a dockerfile in order to be executed on containers.
In order to run this project on a container, just create an image of the dockerfile, then run it while exposing ports (8081:5000) 
for access using localhost and port 8081 from your machine.
