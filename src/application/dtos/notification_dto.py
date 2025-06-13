from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class CreateNotificationDTO:
    title: str
    message: str
    level: str
    metadata: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

@dataclass
class SendNotificationDTO:
    title: str
    message: str
    level: str
    channels: Dict[str, Dict[str, Any]]  # channel_name -> config
    metadata: Optional[Dict[str, Any]] = None
    source: Optional[str] = None