import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

class TelegramPlatform(BasePlatform):
    name = "Telegram"

    async def publish(self, message: str) -> PlatformResult:
        if not settings.telegram_bot_token or not settings.telegram_channel_id:
            return self.failure("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID")

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
                json={"chat_id": settings.telegram_channel_id,
                      "text": message,
                      "disable_web_page_preview": False},
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return self.failure(data.get("description", "Telegram rejected the message"))

            message_id = data["result"]["message_id"]
            username = settings.telegram_channel_username.lstrip("@")
            url = f"https://t.me/{username}/{message_id}" if username else None
            return self.success(url, bool(url))

    async def safe_publish(self, message: str) -> PlatformResult:
        try:
            return await self.publish(message)
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            return self.failure(f"Telegram API error: {exc}")
