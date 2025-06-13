from abc import ABC, abstractmethod
from typing import Dict, Any

from ..dtos.notification_dto import SendNotificationDTO

class NotificationServiceInterface(ABC):
    
    @abstractmethod
    async def send_notification(self, dto: SendNotificationDTO) -> Dict[str, Any]:
        """Send notification to specified channels"""
        pass