# Project Management - Backend
Project/task management for organizations - Backend using Python-django REST framework

# Setup
If you are new to python-django REST framework, follow these steps to start your project

1. Create a folder - "FolderName" and install pip (python packages)
2. Virtual environment creation, Virtualevn installation - "pip install virtualenv"
3. "virtualenv FolderName/" - creates a virtual machine/sandbox.
4. Once created, go to FolderName folder and run - "source bin/activate"
5. Install Django here - "pip install Django==1.9.6"
6. Once successfully installed start project from django admin using - "django-admin startproject ProjectName"
7. After creating a project, go into the project folder and create an app(folder) - "python manage.py startapp AppName"
8. To run the server, go to the project folder and - "python manage.py runserver 0.0.0.0:8000"

For more info about setup - http://www.django-rest-framework.org/tutorial/1-serialization/#setting-up-a-new-environment

# Model Migrations

python manage.py makemigrations AppName
python manage.py migrate AppName
