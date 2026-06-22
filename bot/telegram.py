import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import settings
import aiosqlite

class FraudBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token) if token else None
        self.dp = Dispatcher()
        self._register_handlers()

    def _register_handlers(self):
        @self.dp.message(Command("start"))
        async def start_cmd(message: Message):
            await message.answer(f"🛡 Huginn AI-Охранник\nВаш Chat ID: {message.chat.id}")

        @self.dp.message(Command("stats"))
        async def stats_cmd(message: Message):
            async with aiosqlite.connect(settings.DB_PATH) as db:
                async with db.execute("SELECT COUNT(*) FROM calls WHERE is_fraud = 1") as c:
                    fraud_count = (await c.fetchone())[0]
                await message.answer(f"Статистика: обнаружено {fraud_count} угроз.")

    async def send_alert(self, report):
        if not self.bot or not settings.TG_CHAT_ID: return
        text = f"🚨 **МОШЕННИЧЕСТВО!**\n\n📞 От: {report.caller_info}\n📊 Уверенность: {report.confidence:.1%}\n📝 {report.transcript[:500]}"
        await self.bot.send_message(settings.TG_CHAT_ID, text, parse_mode="Markdown")

    async def run(self):
        if self.bot:
            await self.dp.start_polling(self.bot)
