class BaseFredAPIError(Exception):
    """Base class for all API errors."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidAPIKey(BaseFredAPIError):
    """Error raised when the API Key is invalid."""

    def __init__(self):
        super().__init__(
            "API key must be a 32 character lower-cased alpha-numeric string."
        )


class APIKeyNotFoundError(BaseFredAPIError):
    """Error raised when API key is not found."""

    def __init__(self):
        super().__init__(
            """API key not found. Either set a FRED_API_KEY environment variable or pass your API key to the api_key parameter"""
        )


class FredAPIRequestError(BaseFredAPIError):
    """Error raised when a request to the FRED API fails."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"HTTP response code: {self.status_code} - {self.message}"
