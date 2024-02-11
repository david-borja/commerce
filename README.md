#Django Commands

Create a Django project
django-admin startproject <project-name>

Create a Django app
python3 manage.py startapp <app-name>

https://cs50.harvard.edu/web/2020/notes/4/#django-models

Start the Django web server
python3 manage.py runserver

After changes in <project_name>/models.py
python3 manage.py makemigrations

Migrate changes to database
python3 manage.py migrate

Remove all data from the database
python3 manage.py flush

Seed database with development data
python3 manage.py seed_db

Create Django Admin
python3 manage.py createsuperuser

Tailwind config
https://pypi.org/project/django-tailwind/

To start Django Tailwind in development mode, run the following command in a terminal:
python3 manage.py tailwind start
