from typing import Any
from flask import request
from flask_socketio import SocketIO, emit, join_room # type: ignore

socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")

@socketio.on('connect')
def connect() -> None:
    print(f"Client connected: {request.sid}") # type: ignore

@socketio.on('disconnect')
def disconnect() -> None:
    print(f"Client disconnected: {request.sid}") # type: ignore

@socketio.on('join_admin_room')
def handle_join_admin_room(payload: dict[str, Any]) -> None:
    user_id: int = payload.get('user_id', 0)
    role: str = payload.get('role', "")

    if user_id > 0 and role == "ADMINISTRATOR":
        join_room('admins')
        print(f"Admin {user_id} joined admins room")
        emit('connected', {'message': 'Welcome admin!'}, to=request.sid) # type: ignore

def send_to_room(room: str, event: str, data: dict[str, Any]) -> None:
    socketio.emit(event, data, to=room) # type: ignore