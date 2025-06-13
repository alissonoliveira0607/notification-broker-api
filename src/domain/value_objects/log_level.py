from enum import Enum
from typing import Dict, Tuple

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    DISASTER = "DISASTER"
    
    @property
    def emoji(self) -> str:
        emojis = {
            LogLevel.INFO: "ℹ️",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌",
            LogLevel.CRITICAL: "🚨",
            LogLevel.DISASTER: "💀"
        }
        return emojis[self]
    
    @property
    def slack_color(self) -> str:
        colors = {
            LogLevel.INFO: "#36a64f",      # green
            LogLevel.WARNING: "#ff9500",   # orange
            LogLevel.ERROR: "#ff0000",     # red
            LogLevel.CRITICAL: "#8b0000",  # dark red
            LogLevel.DISASTER: "#4b0082"   # indigo
        }
        return colors[self]
    
    @property
    def priority(self) -> int:
        priorities = {
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4,
            LogLevel.DISASTER: 5
        }
        return priorities[self]
