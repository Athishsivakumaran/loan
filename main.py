import os
from flask import Flask
from applications import config
from applications.config import LocalDevelopmentConfig
from applications.database import db

app=None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()

from applications.controllers import *

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)


