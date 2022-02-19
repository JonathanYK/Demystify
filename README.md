# Demystify project

The main purpose of this project is managing sessions using Flask framework in front of an SQLite database (using SQLAlchemy as ORM).
Supported routes splitted to blueprints, 2 configurations defined in order to execute this project both on test and production environments.
In order to ensure that the access to db is thread safe - scoped_session of SQLAlchemy is used.

The project has both unit and functionality tests, designed using Pytest framework.

This project has a dockerfile in order to be executed on containers.
In order to run this project on a container, just create an image of the dockerfile, then run it while exposing ports (8081:5000) 
for access using localhost and port 8081 from your machine.
