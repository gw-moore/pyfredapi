"""The exceptions module contains the custom exceptions for pyfredapi."""


class BaseFredAPIError(Exception):
    def __init__(self, message):
        """Base class for all API errors."""  # noqa: D401
        self.message = message

    def __str__(self):
        return self.message


class InvalidAPIKey(BaseFredAPIError):
    def __init__(self):
        """Error raised when the API Key is invalid."""
        super().__init__(
            "API key must be a 32 character lower-cased alpha-numeric string."
        )


class APIKeyNotFound(BaseFredAPIError):
    def __init__(self):
        """Error raised when FRED_API_KEY not found in the environment."""
        super().__init__(
            """API key not found. Either set a FRED_API_KEY environment variable or pass your API key to the `api_key` parameter."""
        )


class FredAPIRequestError(BaseFredAPIError):
    def __init__(self, message, status_code):
        """Error raised when a request to the FRED API fails."""
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"HTTP response code: {self.status_code} - {self.message}"
