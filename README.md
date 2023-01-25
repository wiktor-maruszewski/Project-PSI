# Project-PSI
authors of Project-PSI repo:
Wiktor Maruszewski
Artur Żarnoch

Project: 
The project concerns the creation of a website using Django framework that allows you to better manage your time using a list of tasks for a given day and special reminders and statistics. It is similar to well - known app "Microsoft To Do".

Update:
Changed relations between Room model and User model):
splitted in three different tables using django ManyToManyFields.
It results in three separated tables between User and Room (user_room, can_finish_task, can_create_task).

# Model bazy danych
![Alt text](db_schema.png?raw=true "Database scheme visualisation")
