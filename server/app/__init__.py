from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.database.pgsql import engine, Base
from app.repositories.user.user_repository import UserRepository
from app.repositories.redis.blacklist_repository import BlacklistRepository
from app.repositories.redis.blocklist_repository import BlocklistRepository
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import MailService, UserService
from app.web_api.controllers.auth.auth_controller import AuthController
from app.web_api.controllers.user.user_controller import UserController
from app.database import get_redis_client, init_redis

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": { "origins": os.getenv("CORS_ORIGINS").split(',') }}, supports_credentials=True)

    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

    app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config["JWT_ALGORITHM"] = "HS256"

    init_redis()

    JWTManager(app)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    user_repository = UserRepository()
    blacklist_repository = BlacklistRepository(get_redis_client(), ttl=3600)
    blocklist_repository = BlocklistRepository(get_redis_client(), block_threshold=3, ttl=60)

    mail_service = MailService()
    auth_service = AuthService(user_repository, blacklist_repository, blocklist_repository)
    user_service = UserService(user_repository, mail_service)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(user_service)

    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(user_controller.blueprint)
    @app.route('/')
    def index():
        return 'Server is running!'

    return app
