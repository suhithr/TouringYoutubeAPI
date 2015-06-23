##Touring YoutubeAPI
This project uses **Youtube Data API** and is packaged as a **Flask** App with a Postgresql Database

Requirements are in the *requirements.txt* file.

To run the app make sure you have all the dependencies installed (preferably a virtualenvironment) and in the terminal type the command 
    
    $python app.py 

You need to install postgresql to use the application. You can get it here. In the config.py you must define your own URI of the format

    postgresql://username:password@localhost:port/database

Note: Postgres installs with a user "postgres" by default, to set a password for it, it's handy (in Ubuntu) to use 
    
    $sudo passwd postgres

to set a new password, otherwise you can enter the command

    $sudo -u postgre psql -c "ALTER USER postgres PASSWORD 'yourdesiredpassword';"