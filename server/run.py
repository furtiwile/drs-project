import signal
import sys
import inspect
from app import create_app
from app.web_socket.socket import socketio

app = create_app()

def handle_shutdown(signal: int, frame: inspect.FrameType | None) -> None: # type: ignore
    print("Shutting down server gracefully...")
    socketio.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown) # type: ignore

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000) # type: ignore
