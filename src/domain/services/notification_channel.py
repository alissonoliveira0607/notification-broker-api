from abc import ABC, abstractmethod
from typing import Any, Dict

from ..entities.notification import Notification

class NotificationChannelInterface(ABC):
    
    @abstractmethod
    async def send(self, notification: Notification, config: Any) -> Dict[str, Any]:
        """Send notification through channel"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Any) -> bool:
        """Validate channel configuration"""
        pass