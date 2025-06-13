from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4, UUID

from ..value_objects.log_level import LogLevel

@dataclass
class Notification:
    id: UUID
    title: str
    message: str
    level: LogLevel
    metadata: Dict[str, Any]
    timestamp: datetime
    source: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        title: str,
        message: str,
        level: LogLevel,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None
    ) -> "Notification":
        return cls(
            id=uuid4(),
            title=title,
            message=message,
            level=level,
            metadata=metadata or {},
            timestamp=datetime.utcnow(),
            source=source
        )
    
    def to_slack_payload(self, config: 'SlackConfig') -> Dict[str, Any]:
        """Generate Slack-formatted payload"""
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        attachment = {
            "color": self.level.slack_color,
            "title": f"{self.level.emoji} {self.title}",
            "text": self.message,
            "fields": [
                {
                    "title": "Level",
                    "value": self.level.value,
                    "short": True
                },
                {
                    "title": "Timestamp",
                    "value": timestamp_str,
                    "short": True
                }
            ],
            "footer": f"Notification ID: {self.id}",
            "ts": int(self.timestamp.timestamp())
        }
        
        if self.source:
            attachment["fields"].append({
                "title": "Source",
                "value": self.source,
                "short": True
            })
        
        if self.metadata:
            metadata_text = "\n".join([f"• *{k}*: {v}" for k, v in self.metadata.items()])
            attachment["fields"].append({
                "title": "Metadata",
                "value": metadata_text,
                "short": False
            })
        
        payload = {
            "attachments": [attachment],
            **config.to_dict()
        }
        
        return payload
    
    def to_telegram_payload(self) -> str:
        """Generate Telegram-formatted message"""
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        message_parts = [
            f"{self.level.emoji} *{self.title}*",
            "",
            f"📝 {self.message}",
            "",
            f"🏷️ *Level:* `{self.level.value}`",
            f"🕐 *Time:* `{timestamp_str}`"
        ]
        
        if self.source:
            message_parts.append(f"🔍 *Source:* `{self.source}`")
        
        if self.metadata:
            message_parts.append("")
            message_parts.append("📊 *Metadata:*")
            for key, value in self.metadata.items():
                message_parts.append(f"• *{key}:* `{value}`")
        
        message_parts.extend([
            "",
            f"🆔 `{self.id}`"
        ])
        
        return "\n".join(message_parts)
