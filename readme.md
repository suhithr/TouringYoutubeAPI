##Touring YoutubeAPI
This project uses **Youtube Data API** and is packaged as a **Flask** App with a Postgresql Database and SQLAlchemy ORM

**Technologies Used**
1.Client Side:

    *HTML with Jinja2 templating

    *CSS

    *Javascript

2. Server Side:

    *Flask

    *PostgreSQL

    *SQLAlchemy ORM

**Requirements** are in the *requirements.txt* file in the repo.

**Installing PostgreSQL**
You need to install postgresql to use the application. You can get it here. In the config.py you must define your own URI of the format

    postgresql://username:password@localhost:port/database

Note: Postgres installs with a user "postgres" by default, to set a password for it, it's handy (in Ubuntu) to use 
    
    $sudo passwd postgres

to set a new password, otherwise you can enter the command

    $sudo -u postgre psql -c "ALTER USER postgres PASSWORD 'yourdesiredpassword';"

The **server** routes being used are

*'/'

*'/search'

*'/result'


The database has 2 tables *searched2* and *selected1*

*searched2->{id, term, response, timeofsearch}

*selected1->{id, term_id, response, timeofrequest}

These are used to store the data from the search, and also from the fetching of statistics


The **modules** used are:

*Flask 'pip install Flask'

*Flask-SQLAlchemy 'pip install Flask-SQLAlchemy'

*google-api-python-client [Google Developers](https://developers.google.com/api-client-library/python/)

*psycopg2 'pip install psycopg2' Note that it requires PostgreSQL to be installed first, can install [PostgreSQL from](http://www.postgresql.org/)

*SQLAlchemy 'pip install sqlalchemy'

I recommend you install all these in a virtual environment 'pip install virtualenv'


**Build Instructions** (Recommended to do this in a virtual environment)

*Set the environment, up by installing all the requirements as listed above

*Copy the repository to the appropriate folder

*Create a config.py file with contents:
'''
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'a-secret-key'
    SQLALCHEMY_DATABASE_URI = 'the-uri-of-your-database'
'''
Set DEBUG to True if it's a development server for ease of use. Change the line in app.py 'app.config.from_object("config.ProductionConfig")' to 'app.config.from_object("config.BaseConfig")'

*Run '$python db_create.py'

*Run '$python app.py' 

The server should be up and running now.


**Screenshots**
*![Homepage](/screenshots/HomePage.png)
*![Search](/screenshots/Search.png)
*![Result](/screenshots/Result.png)
