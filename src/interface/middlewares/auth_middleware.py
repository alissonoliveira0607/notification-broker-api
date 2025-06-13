from functools import wraps
from flask import request, jsonify
from typing import Callable

from interface.exceptions.api_exceptions import AuthenticationException
from infrastructure.config.settings import Settings

def require_api_key(settings: Settings) -> Callable:
    """Decorator to require API key authentication"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")
            
            if not api_key:
                raise AuthenticationException("API key is required")
            
            # Remove 'Bearer ' prefix if present
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            
            if api_key != settings.API_KEY:
                raise AuthenticationException("Invalid API key")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
