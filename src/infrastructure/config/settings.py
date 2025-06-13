import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class Settings:
    # API Configuration
    API_KEY: str
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            API_KEY=os.getenv("API_KEY", "your-secret-api-key"),
            DEBUG=os.getenv("DEBUG", "False").lower() == "true",
            HOST=os.getenv("HOST", "0.0.0.0"),
            PORT=int(os.getenv("PORT", "8000")),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO")
        )