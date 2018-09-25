This is the repository of team Sunshine - DECO3801

The repository will be used for the ShareShed Project.

Installation

Before installation, make sure you have these program installed:
- python 3 (at least 3.5)
- mysql

It is recommended to create a virtual environment to keep the dependency of
this project isolated from other project.

To create virtual environment, simply run:
Python3 -m venv virtual_environment_name

Then activate it by:
Linux/Mac:
source virtual_environment_name/bin/activate
Windows:
virtual_environment_name/Scripts/activate.bat

Then install all the dependencies by running:
pip install -r requirements.txt

This command will install all dependencies listed in the requirements.txt.

After you installed all the dependencies, make sure to set environment variables

export SECRET_KEY=<Application secret key>
export DB_USER=<Database user>
export DB_PASSWORD=<Database user password>
export DB_NAME=<Database name>
export DB_HOST=<Database url>
export STRIPE_PUBLIC=<Stripe public key>
export STRIPE_SECRET=<Stripe secret key>
export EMAIL_HOST=<Email host>
export EMAIL_HOST_USER=<Email address>
export EMAIL_HOST_PASSWORD=<Email password>
export EMAIL_HOST_PORT=<Email port, default for ssl should be 465>

These environment will be imported from share_shed/settings.py.

To migrate the database, run:
python manage.py migrate

To add an admin account, run:
python manage.py createsuperuser

After the migration, you can run the application using:
python manage.py runserver

You can now open the application from the browser,
the url should be shown in the terminal.
