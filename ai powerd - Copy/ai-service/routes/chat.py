from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from main import limiter
import bleach
from pydantic import BaseModel


router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.get("/limited")
@limiter.limit("5/minute")
async def limited_route():
    return {"message": "This route is rate limited"}

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

class InputModel(BaseModel):
    text: str

@router.post("/sanitize")
async def sanitize_input(input: InputModel):
    clean_text = bleach.clean(input.text)
    return {"clean_text": clean_text}