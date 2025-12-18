from flask import Flask
from app.database import engine, Base
from app.domain.models.User import User

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    @app.route('/')
    def index():
        return 'Server is running!'

    return app
