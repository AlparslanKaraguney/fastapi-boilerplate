"""
Custom Exceptions
"""

from fastapi import status as status
from typing import Optional


class ValidationError(Exception):
    """
    Validation Error
    cause of missing required params
    """

    def __init__(self, exc):
        super().__init__(exc)


class AuthenticationFailedError(Exception):
    """
    Authentication Failed Error
    cause of any errors on decoding jwt token
    """

    def __init__(self, exc):
        super().__init__(exc)


class CustomException(Exception):
    """
    Base Custom Execption
    to printing error message
    """

    def __init__(
        self, status_code=status.HTTP_400_BAD_REQUEST, exc="Bad Request"
    ):
        self.status_code = status_code
        super().__init__(exc)


class PermissionDeniedException(Exception):
    """
    Permission denied
    """

    def __init__(self, exc):
        super().__init__(exc)
