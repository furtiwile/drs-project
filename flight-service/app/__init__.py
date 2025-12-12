from flask import Flask

def create_app():
    app = Flask(__name__)
    # Config and blueprints can be registered here
    @app.route('/')
    def index():
        return 'Flight Service is running!'
    return app
