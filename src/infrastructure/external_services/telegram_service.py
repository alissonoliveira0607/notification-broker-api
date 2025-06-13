import aiohttp
import logging
from typing import Dict, Any

from domain.entities.notification import Notification
from domain.value_objects.channel_config import TelegramConfig
from domain.services.notification_channel import NotificationChannelInterface

logger = logging.getLogger(__name__)

class TelegramNotificationChannel(NotificationChannelInterface):
    
    async def send(self, notification: Notification, config: TelegramConfig) -> Dict[str, Any]:
        """Send notification to Telegram"""
        message_text = notification.to_telegram_payload()
        
        payload = {
            "chat_id": config.chat_id,
            "text": message_text,
            "parse_mode": config.parse_mode
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config.api_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                response_data = await response.json()
                
                if response.status == 200 and response_data.get("ok"):
                    logger.info(f"Telegram notification sent successfully: {notification.id}")
                    return {"status": "sent", "response": response_data}
                else:
                    error_desc = response_data.get("description", "Unknown error")
                    logger.error(f"Failed to send Telegram notification: {error_desc}")
                    raise Exception(f"Telegram API error: {error_desc}")
    
    def validate_config(self, config: TelegramConfig) -> bool:
        """Validate Telegram configuration"""
        return bool(config.bot_token and config.chat_id)