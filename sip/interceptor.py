import asyncio
import aiosip
import logging
from typing import AsyncIterator
from config import settings

class SipInterceptor:
    def __init__(self, host=settings.SIP_HOST, port=settings.SIP_PORT):
        self.host = host
        self.port = port
        self.is_connected = False
        self.app = None

    async def start(self):
        try:
            self.app = aiosip.Application()
            # In a production setup, we would register here
            # await self.app.register(settings.SIP_HOST, settings.SIP_USER, settings.SIP_PASSWORD)
            logging.info(f"SIP Interceptor listening on {self.host}:{self.port}")
            self.is_connected = True
        except Exception as e:
            logging.error(f"Failed to start SIP: {e}")

    async def on_invite(self, dialog):
        # Handle incoming SIP INVITE
        # In actual implementation, we would extract RTP stream here
        pass

    def shutdown(self):
        if self.app:
            # self.app.stop()
            pass
        self.is_connected = False
