# Genskill-Project

#Introduction

This repository contains the web app to maintain a list of tasks. It is part of the Genskill fullstack development bootcamp final project.
It supports the following features.

1. Multiple user authentication.
2. Add tasks, date, points to remember for the task and the urgency of the task.
3. All tasks will be displayed on a table. Any task not completed within the given date of task is considered as an overdue task.
4. Click the task to view details of the task.
5. Edit task allows one to edit any aspect of the task and even mark it as complete.
6. Clicking the `Date` header sorts the tasks by date.
7. Clicking the `Urgency` header sorts the tasks by urgency.
8. Clicking the `Status` header shows the completed and incomplete tasks separately.
9. Clicking `Weekly Schedule` allows one to view all tasks to be completed within the current week.


# Setting up

1. Clone repository
2. Create a virtualenv and activate it
3. Install dependencies using `pip install -r requirements.txt`
4. Create the necessary datbase using `createdb todolist`
5. `export FLASK_APP=todolist` to set the application
6. `flask initdb` to create the initial database
7. `flask run` to start the app.

