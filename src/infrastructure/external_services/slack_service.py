import aiohttp
import logging
from typing import Dict, Any

from domain.entities.notification import Notification
from domain.value_objects.channel_config import SlackConfig
from domain.services.notification_channel import NotificationChannelInterface

logger = logging.getLogger(__name__)

class SlackNotificationChannel(NotificationChannelInterface):
    
    async def send(self, notification: Notification, config: SlackConfig) -> Dict[str, Any]:
        """Send notification to Slack"""
        try:
            # Validate configuration first
            if not self.validate_config(config):
                raise Exception(f"Invalid Slack configuration: webhook URL must start with https://hooks.slack.com/")
            
            payload = notification.to_slack_payload(config)
            logger.debug(f"Sending Slack notification: {notification.id} to {config.webhook_url}")
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    config.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        if response_text.strip() == "ok":
                            logger.info(f"Slack notification sent successfully: {notification.id}")
                            return {"status": "sent", "response": response_text}
                        else:
                            logger.warning(f"Slack response unexpected: {response_text}")
                            return {"status": "sent", "response": response_text}
                    else:
                        error_msg = f"Slack webhook error (HTTP {response.status}): {response_text}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                        
        except aiohttp.ClientError as e:
            error_msg = f"Network error sending to Slack: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            if "Invalid Slack configuration" in str(e) or "Slack webhook error" in str(e) or "Network error" in str(e):
                raise
            else:
                error_msg = f"Unexpected error sending Slack notification: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
    
    def validate_config(self, config: SlackConfig) -> bool:
        """Validate Slack configuration"""
        return (
            config and
            hasattr(config, 'webhook_url') and
            config.webhook_url and
            isinstance(config.webhook_url, str) and
            config.webhook_url.startswith("https://hooks.slack.com/")
        )