class DomainException(Exception):
    """Base domain exception"""
    pass

class InvalidNotificationDataException(DomainException):
    """Raised when notification data is invalid"""
    pass

class UnsupportedChannelException(DomainException):
    """Raised when trying to use unsupported notification channel"""
    pass