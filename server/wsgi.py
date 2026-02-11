"""
WSGI entry point for production deployment with Gunicorn.
This file is used by Gunicorn to run the Flask application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app()

application = app

if __name__ == "__main__":
    port = int(os.getenv('SERVER_PORT', 5000))
    app.run(host='0.0.0.0', port=port)