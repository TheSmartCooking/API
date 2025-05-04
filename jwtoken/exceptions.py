class TokenError(Exception):
    """Custom exception for token-related errors."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
