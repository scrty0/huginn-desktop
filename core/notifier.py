import asyncio
from aiogram import Bot
from .models import AlertEvent, FraudReport
from api.websocket_manager import manager
from config import settings

class Notifier:
    def __init__(self):
        self.bot = Bot(token=settings.TG_BOT_TOKEN) if settings.TG_BOT_TOKEN else None

    async def send_telegram(self, report: FraudReport):
        if not self.bot or not settings.TG_CHAT_ID:
            return
        text = f"🚨 МОШЕННИЧЕСТВО!\nУверенность: {report.confidence:.1%}\nКатегория: {report.trigger_category}\nТекст: {report.transcript[:200]}..."
        await self.bot.send_message(settings.TG_CHAT_ID, text)

    async def broadcast(self, event: AlertEvent):
        # 1. WebSocket
        await manager.broadcast(event)

        # 2. Telegram
        if event.type == "fraud_detected" and event.report:
            await self.send_telegram(event.report)

        # 3. Sound (skipped in headless env)
