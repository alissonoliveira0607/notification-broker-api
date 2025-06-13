class APIException(Exception):
    """Base API exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationException(APIException):
    """Authentication failed exception"""
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, 401)

class ValidationException(APIException):
    """Request validation exception"""
    def __init__(self, message: str):
        super().__init__(message, 400)