from typing import Dict, Any, Optional
from dataclasses import asdict

from application.dtos.notification_dto import SendNotificationDTO
from interface.exceptions.api_exceptions import ValidationException

class NotificationSerializer:
    
    @staticmethod
    def deserialize_send_request(data: Dict[str, Any]) -> SendNotificationDTO:
        """Deserialize send notification request"""
        try:
            # Extract channel configs from headers and body
            channels = {}
            
            # Slack configuration
            slack_config = {}
            if "slack_webhook_url" in data:
                slack_config["webhook_url"] = data["slack_webhook_url"]
            if "slack" in data.get("channels", {}):
                slack_config.update(data["channels"]["slack"])
            
            # Only add slack channel if we have a webhook URL
            if slack_config.get("webhook_url"):
                channels["slack"] = slack_config
            
            # Telegram configuration
            telegram_config = {}
            if "telegram_bot_token" in data:
                telegram_config["bot_token"] = data["telegram_bot_token"]
            if "telegram_chat_id" in data:
                telegram_config["chat_id"] = data["telegram_chat_id"]
            if "telegram" in data.get("channels", {}):
                telegram_config.update(data["channels"]["telegram"])
            
            # Only add telegram channel if we have both bot_token and chat_id
            if telegram_config.get("bot_token") and telegram_config.get("chat_id"):
                channels["telegram"] = telegram_config
            
            if not channels:
                raise ValidationException("At least one notification channel must be configured with valid parameters")
            
            return SendNotificationDTO(
                title=data["title"],
                message=data["message"],
                level=data["level"],
                channels=channels,
                metadata=data.get("metadata"),
                source=data.get("source")
            )
            
        except KeyError as e:
            raise ValidationException(f"Missing required field: {e}")
        except Exception as e:
            raise ValidationException(f"Invalid request data: {str(e)}")