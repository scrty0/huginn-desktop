from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: any):
        if hasattr(message, "model_dump"):
            data = message.model_dump()
        else:
            data = message

        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except:
                dead.append(connection)

        for d in dead:
            self.disconnect(d)

manager = ConnectionManager()
