from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # Store active connections: user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        # Remove the websocket from active connections
        for user_id, connection in self.active_connections.items():
            if connection == websocket:
                del self.active_connections[user_id]
                break

    def add_connection(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    async def send_personal_message(self, user_id: int, message: dict):
        """
        Send a message to a specific user
        """
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """
        Broadcast a message to all connected users
        """
        for connection in self.active_connections.values():
            await connection.send_json(message)

    async def broadcast_except(self, message: dict, exclude_user_id: int):
        """
        Broadcast a message to all connected users except one
        """
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user_id:
                await connection.send_json(message) 