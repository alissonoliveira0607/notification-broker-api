from typing import Dict, List, Optional
from uuid import UUID

from domain.entities.notification import Notification
from domain.repositories.notification_repository import NotificationRepositoryInterface

class InMemoryNotificationRepository(NotificationRepositoryInterface):
    
    def __init__(self):
        self._notifications: Dict[UUID, Notification] = {}
    
    async def save(self, notification: Notification) -> None:
        """Save notification to in-memory storage"""
        self._notifications[notification.id] = notification
    
    async def find_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """Find notification by ID"""
        return self._notifications.get(notification_id)
    
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Notification]:
        """Find all notifications with pagination"""
        notifications = list(self._notifications.values())
        notifications.sort(key=lambda n: n.timestamp, reverse=True)
        return notifications[offset:offset + limit]