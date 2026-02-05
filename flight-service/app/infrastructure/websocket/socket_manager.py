"""
WebSocket manager for real-time flight notifications
Following Clean Architecture - Infrastructure layer
"""
from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict
from ...domain.types.websocket_types import FlightNotificationData
from app.utils.logger_service import get_logger

logger = get_logger(__name__)

socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')


class SocketManager:
    """Manages WebSocket connections and real-time notifications"""
    
    def __init__(self):
        self.socketio = socketio
        self._connected_users: Dict[str, str] = {}  # sid -> user_id mapping
        
    def init_app(self, app):
        """Initialize SocketIO with Flask app"""
        self.socketio.init_app(app)
        self._register_handlers()
    
    def _register_handlers(self):
        """Register WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            from flask import request as flask_request
            sid = getattr(flask_request, 'sid', 'unknown')
            logger.info(f"Client connected: {sid}")
            emit('connected', {'message': 'Connected to flight service'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            from flask import request as flask_request
            sid = getattr(flask_request, 'sid', None)
            logger.info(f"Client disconnected: {sid}")
            if sid and sid in self._connected_users:
                del self._connected_users[sid]
        
        @self.socketio.on('join_admin_room')
        def handle_join_admin_room(data):
            """Admin joins the room to receive new flight notifications"""
            from flask import request as flask_request
            user_id = data.get('user_id')
            role = data.get('role')
            
            if role == 'ADMINISTRATOR':
                join_room('admin_room')
                sid = getattr(flask_request, 'sid', None)
                if sid:
                    self._connected_users[sid] = user_id
                logger.info(f"Admin {user_id} joined admin_room")
                emit('joined_admin_room', {'message': 'Successfully joined admin room'})
        
        @self.socketio.on('leave_admin_room')
        def handle_leave_admin_room():
            """Admin leaves the admin room"""
            leave_room('admin_room')
            logger.info(f"Admin left admin_room")
            emit('left_admin_room', {'message': 'Left admin room'})
        
        @self.socketio.on('join_manager_room')
        def handle_join_manager_room(data):
            """Manager joins room to receive flight status updates"""
            from flask import request as flask_request
            user_id = data.get('user_id')
            role = data.get('role')
            
            if role in ['MANAGER', 'ADMINISTRATOR']:
                room = f'manager_{user_id}'
                join_room(room)
                sid = getattr(flask_request, 'sid', None)
                if sid:
                    self._connected_users[sid] = user_id
        
        @self.socketio.on('leave_manager_room')
        def handle_leave_manager_room(data):
            """Manager leaves the manager room"""
            user_id = data.get('user_id')
            role = data.get('role')
            
            if role in ['MANAGER', 'ADMINISTRATOR']:
                room = f'manager_{user_id}'
                leave_room(room)
                logger.info(f"Manager {user_id} left manager_room")
                emit('left_manager_room', {'message': 'Left manager room'})
        
        @self.socketio.on('join_flight_room')
        def handle_join_flight_room(data):
            """Client joins a specific flight room to receive updates for that flight"""
            flight_id = data.get('flight_id')
            
            if flight_id:
                room = f'flight_{flight_id}'
                join_room(room)
                logger.info(f"Client joined flight room: {room}")
                emit('joined_flight_room', {'message': f'Successfully joined flight room for flight {flight_id}'})
        
        @self.socketio.on('leave_flight_room')
        def handle_leave_flight_room(data):
            """Client leaves a specific flight room"""
            flight_id = data.get('flight_id')
            
            if flight_id:
                room = f'flight_{flight_id}'
                leave_room(room)
                logger.info(f"Client left flight room: {room}")
                emit('left_flight_room', {'message': f'Left flight room for flight {flight_id}'})
    
    def notify_new_flight(self, flight_data: FlightNotificationData):
        """Notify admins about new pending flight"""
        try:
            self.socketio.emit('new_flight_pending', flight_data, to='admin_room')
            logger.info(f"Notified admins about new flight: {flight_data.get('flight_id')}")
        except Exception as e:
            logger.error(f"Error notifying new flight: {str(e)}")
    
    def notify_flight_status_update(self, manager_id: int, flight_data: FlightNotificationData):
        """Notify manager about flight status update (approved/rejected)"""
        try:
            room = f'manager_{manager_id}'
            self.socketio.emit('flight_status_updated', flight_data, to=room)
            logger.info(f"Notified manager {manager_id} about flight status update")
        except Exception as e:
            logger.error(f"Error notifying flight status update: {str(e)}")
    
    def notify_flight_cancelled(self, flight_data: FlightNotificationData):
        """Broadcast flight cancellation to all connected clients OR notify specific flight room"""
        try:
            flight_id = flight_data.get('flight_id')
            if flight_id:
                room = f'flight_{flight_id}'
                self.socketio.emit('flight_cancelled', flight_data, to=room)
                logger.info(f"Notified flight room {room} about cancellation")
            else:
                # Fallback to broadcast if no flight_id
                self.socketio.emit('flight_cancelled', flight_data)
                logger.info(f"Broadcasted flight cancellation: {flight_id}")
        except Exception as e:
            logger.error(f"Error notifying flight cancellation: {str(e)}")
    
    def notify_flight_started(self, flight_data: FlightNotificationData):
        """Broadcast that a flight has started OR notify specific flight room"""
        try:
            flight_id = flight_data.get('flight_id')
            if flight_id:
                room = f'flight_{flight_id}'
                self.socketio.emit('flight_started', flight_data, to=room)
                logger.info(f"Notified flight room {room} about flight start")
            else:
                # Fallback to broadcast if no flight_id
                self.socketio.emit('flight_started', flight_data)
                logger.info(f"Broadcasted flight started: {flight_id}")
        except Exception as e:
            logger.error(f"Error broadcasting flight start: {str(e)}")
    
    def notify_flight_completed(self, flight_data: FlightNotificationData):
        """Broadcast that a flight has completed OR notify specific flight room"""
        try:
            flight_id = flight_data.get('flight_id')
            if flight_id:
                room = f'flight_{flight_id}'
                self.socketio.emit('flight_completed', flight_data, to=room)
                logger.info(f"Notified flight room {room} about flight completion")
            else:
                # Fallback to broadcast if no flight_id
                self.socketio.emit('flight_completed', flight_data)
                logger.info(f"Broadcasted flight completed: {flight_id}")
        except Exception as e:
            logger.error(f"Error broadcasting flight completion: {str(e)}")


def init_socketio(app):
    """Initialize SocketIO with Flask app and return both socketio and socket_manager instance"""
    socket_manager = SocketManager()
    socket_manager.init_app(app)
    return socket_manager
