from flask import Flask
from app.database import engine, Base
from app.domain.models.User import User
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.web_api.controllers.user_controller import UserController

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    user_repository = UserRepository()
    user_service = UserService(user_repository)
    user_controller = UserController(user_service)

    app.register_blueprint(user_controller.blueprint)
    @app.route('/')
    def index():
        return 'Server is running!'

    return app
