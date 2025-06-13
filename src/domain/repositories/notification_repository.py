from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.notification import Notification

class NotificationRepositoryInterface(ABC):
    
    @abstractmethod
    async def save(self, notification: Notification) -> None:
        """Save notification to storage"""
        pass
    
    @abstractmethod
    async def find_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """Find notification by ID"""
        pass
    
    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Notification]:
        """Find all notifications with pagination"""
        pass