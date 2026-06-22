import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from config import settings
from api.websocket_manager import manager
from core.stt import SpeechToText
from core.analyzer import FraudAnalyzer
from core.notifier import Notifier
from bot.telegram import FraudBot

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.stt = SpeechToText()
    app.state.analyzer = FraudAnalyzer()
    app.state.notifier = Notifier()
    if settings.TG_BOT_TOKEN:
        app.state.bot = FraudBot(settings.TG_BOT_TOKEN)
        asyncio.create_task(app.state.bot.run())
    yield

app = FastAPI(title="Huginn AI-Охранник", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok", "app": "Huginn"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

from api.routes import router as api_router
from api.dashboard import router as dashboard_router
app.include_router(api_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
