# README

## Get Started

- python3 manage.py seed_db
- python3 manage.py runserver
- python3 manage.py tailwind start

## Django Models

<https://cs50.harvard.edu/web/2020/notes/4/#django-models>

## Django's Model Field Reference

<https://docs.djangoproject.com/en/4.0/ref/models/fields/>

## Django Forms

<https://docs.djangoproject.com/en/4.0/topics/forms/>

## Django Login Required Decorator

<https://docs.djangoproject.com/en/4.0/topics/auth/default/#the-login-required-decorator>

## Create a Django project

django-admin startproject project_name

or python3 -m django startproject project_name

## Create a Django app

python3 manage.py startapp app_name

## Start the Django web server

python3 manage.py runserver

## After changes in <project_name>/models.py

python3 manage.py makemigrations

## Migrate changes to database

python3 manage.py migrate

## Remove all data from the database

python3 manage.py flush

## Seed database with development data

python3 manage.py seed_db

## Create Django Admin

python3 manage.py createsuperuser

## Tailwind config

<https://pypi.org/project/django-tailwind/>

## Start Django Tailwind in development mode

python3 manage.py tailwind start
