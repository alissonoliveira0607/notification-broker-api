from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class SlackConfig:
    webhook_url: str
    channel: Optional[str] = None
    username: Optional[str] = "NotificationBot"
    
    def to_dict(self) -> Dict[str, Any]:
        config = {"username": self.username}
        if self.channel:
            config["channel"] = self.channel
        return config

@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str
    parse_mode: str = "Markdown"
    
    @property
    def api_url(self) -> str:
        return f"https://api.telegram.org/bot{self.bot_token}/sendMessage"