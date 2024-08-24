To run the project on your PC run below commands in the order they are arranged
Make sure python is installed on your PC whe nyou try to run the project.

Install virtual environment
pip install virtualenv

Create virtual environment
python -m venv env

Activate virtual environment
env\scripts\activate.bat

Install required dependecies
pip install -r requirements.txt

Run the app
python manage.py runserver


If you want to start the app with a new database, delete db.sqlite3 then run below commands.
python manage.py makemigrations

Then make migrations
python manage.py migrate

Then create admin account by running below command.
python manage.py createsuperuser

Now run the app.
python manage.py runserver