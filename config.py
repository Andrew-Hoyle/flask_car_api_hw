import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Give access to the project in ANY OS we find ourselves in
# Allow outside files/folders to be added to the project from the
# base directory

class Config():
    """
        Set Config variables for the flask app.
        Using Environment variables where available otherwise
        create the config variable if not done already.
    """
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI ='postgresql://postgres:hibernation716@127.0.0.1.5432/drone_collection'

    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turn off update messages from the sqlalchemy
