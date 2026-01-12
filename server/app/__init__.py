from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from app.database import engine, Base
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.web_api.controllers.auth_controller import AuthController
from app.web_api.controllers.user_controller import UserController

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config["JWT_ALGORITHM"] = "HS256"

    JWTManager(app)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    user_repository = UserRepository()

    auth_service = AuthService(user_repository)
    user_service = UserService(user_repository)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(user_service)

    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(user_controller.blueprint)
    @app.route('/')
    def index():
        return 'Server is running!'

    return app
