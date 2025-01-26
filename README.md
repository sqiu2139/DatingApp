# Instruction on how to use the demo

## Overview
Currently, the app is built on top of [flask](https://flask.palletsprojects.com/en/stable/), as we are still prototyping the work, we use the 
sqllite to as the temporary database. Backend interacts with database through ORM library [sqlalchemy](https://www.sqlalchemy.org/). The frontend
are simple HTML with css and js query inside. Some important files are:

* app.py - file that defines the main endpoints and function to start the server
* model.py - defines the data model for database
* config.py - defines the setup for database
* ./templates - html pages for endpoints
* ./migrations - scripts used for database schema change
* ./venv library root
* ./instance - automatically generated database data

## Start the server
simply run
```
flask run
```
This will set up the app on a localhost, typically on port 5000

## Change the database
When you change or add a new data model, you need to update the database schema
firstly run
```
flask db migrate -m "{The description of the change you made}"
```
Then run
```
flask db upgrade
```
