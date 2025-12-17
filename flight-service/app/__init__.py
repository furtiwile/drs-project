import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to ensure they are registered
from .models import *

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB2_URL', 'postgresql://user:password@localhost:27018/flights_db')
    app.config['SQLALCHEMY_BINDS'] = {
        'users': os.environ.get('DB1_URL', 'postgresql://user:password@localhost:27017/users_db')
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Config and blueprints can be registered here
    @app.route('/')
    def index():
        return 'Flight Service is running!'

    return app
