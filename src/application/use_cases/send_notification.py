from typing import Dict, Any, List
import asyncio
import logging

from application.dtos.notification_dto import SendNotificationDTO
from application.interfaces.notification_service import NotificationServiceInterface
from domain.entities.notification import Notification
from domain.value_objects.log_level import LogLevel
from domain.value_objects.channel_config import SlackConfig, TelegramConfig
from domain.repositories.notification_repository import NotificationRepositoryInterface
from domain.services.notification_channel import NotificationChannelInterface
from domain.exceptions.domain_exceptions import InvalidNotificationDataException, UnsupportedChannelException

logger = logging.getLogger(__name__)

class SendNotificationUseCase(NotificationServiceInterface):
    
    def __init__(
        self,
        notification_repository: NotificationRepositoryInterface,
        slack_channel: NotificationChannelInterface,
        telegram_channel: NotificationChannelInterface
    ):
        self._notification_repository = notification_repository
        self._channels = {
            "slack": slack_channel,
            "telegram": telegram_channel
        }
    
    async def send_notification(self, dto: SendNotificationDTO) -> Dict[str, Any]:
        """Send notification to specified channels"""
        try:
            # Validate log level
            try:
                log_level = LogLevel(dto.level.upper())
            except ValueError:
                raise InvalidNotificationDataException(f"Invalid log level: {dto.level}")
            
            # Create notification entity
            notification = Notification.create(
                title=dto.title,
                message=dto.message,
                level=log_level,
                metadata=dto.metadata,
                source=dto.source
            )
            
            # Save notification
            await self._notification_repository.save(notification)
            
            # Send to channels asynchronously
            send_tasks = []
            channel_names = []
            
            for channel_name, channel_config in dto.channels.items():
                if channel_name not in self._channels:
                    logger.warning(f"Unsupported channel: {channel_name}")
                    continue
                
                task = self._send_to_channel(notification, channel_name, channel_config)
                send_tasks.append(task)
                channel_names.append(channel_name)
            
            if not send_tasks:
                raise UnsupportedChannelException("No supported channels specified")
            
            # Wait for all sends to complete
            results = await asyncio.gather(*send_tasks, return_exceptions=True)
            
            # Process results
            channel_results = {}
            for i, channel_name in enumerate(channel_names):
                result = results[i]
                if isinstance(result, Exception):
                    logger.error(f"Error sending to {channel_name}: {str(result)}")
                    channel_results[channel_name] = {
                        "success": False,
                        "error": str(result)
                    }
                else:
                    channel_results[channel_name] = {
                        "success": True,
                        "response": result
                    }
            
            return {
                "notification_id": str(notification.id),
                "timestamp": notification.timestamp.isoformat(),
                "channels": channel_results
            }
            
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            raise
    
    async def _send_to_channel(
        self,
        notification: Notification,
        channel_name: str,
        channel_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send notification to specific channel"""
        try:
            channel = self._channels[channel_name]
            
            # Convert config dict to appropriate config object
            if channel_name == "slack":
                config = SlackConfig(**channel_config)
            elif channel_name == "telegram":
                config = TelegramConfig(**channel_config)
            else:
                raise UnsupportedChannelException(f"Unsupported channel: {channel_name}")
            
            # Validate and send
            if not channel.validate_config(config):
                raise InvalidNotificationDataException(f"Invalid {channel_name} configuration")
            
            return await channel.send(notification, config)
            
        except (TypeError, ValueError) as e:
            error_msg = f"Invalid {channel_name} configuration parameters: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            # Re-raise with more context if needed
            if isinstance(e, (UnsupportedChannelException, InvalidNotificationDataException)):
                raise
            else:
                error_msg = f"Error sending to {channel_name}: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
