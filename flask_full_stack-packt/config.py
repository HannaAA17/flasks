import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_SETTINGS = [
    {
        'host': 'mongodb+srv://HannaMonogoDB:<password>@cluster0.f0hywtc.mongodb.net/flask-template'.replace('<password>', 'HannaMonogoDB'),
    }
]