"""
WSGI entry point for production deployment with Gunicorn.
This file is used by Gunicorn to run the Flask application with gevent workers.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

app, socketio = create_app()

# For Gunicorn, we expose the SocketIO application
# The gevent worker will handle the WebSocket connections
application = socketio

if __name__ == "__main__":
    port = int(os.getenv('FLIGHT_SERVICE_PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
