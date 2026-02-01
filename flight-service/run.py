from dotenv import load_dotenv
import os
load_dotenv()

from app import create_app

if __name__ == '__main__':
    app, socketio = create_app()
    
    # Enable debug mode in development
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('FLIGHT_SERVICE_HOST', '0.0.0.0')
    port = int(os.getenv('FLIGHT_SERVICE_PORT', 5555))
    
    # Run with socketio support
    socketio.run(app, host=host, port=port, debug=debug_mode, allow_unsafe_werkzeug=True)


        