from typing import Any, Optional
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class BaseContent(BaseModel):
    """
    Base content model, same meaning with `response body`
    """

    success: bool
    message: str
    data: Any = {}


class BaseResponse(JSONResponse):
    """
    Base JSON response model, includes all
    properties of a response
    >>> BaseResponse(200, True, "msg", {"me":"hi"})
    """

    def __init__(
        self,
        status_code: int,
        success: bool,
        message: str,
        data: Any,
        headers: dict = None,
    ) -> None:
        content = jsonable_encoder(
            BaseContent(success=success, message=message, data=data)
        )
        super().__init__(content, status_code, headers)


class SuccessResponse(BaseResponse):
    """
    Success JSON response model, its enough
    just passing a data
    >>> SuccessResponse({"me":"hi"})
    """

    def __init__(
        self,
        data: Optional[Any] = None,
        message: Optional[str] = "ok",
        headers: dict = None,
    ):
        super().__init__(
            status_code=status.HTTP_200_OK,
            success=True,
            message=message,
            data=data,
            headers=headers,
        )


class ErrorResponse(BaseResponse):
    """
    Error JSON response model, must be pass
    message and status_code
    >>> ErrorResponse(400, "There is a very big problem")
    """

    def __init__(self, status_code: int, message: str, headers: dict = None):
        super().__init__(
            status_code=status_code,
            success=False,
            message=message,
            data=None,
            headers=headers,
        )
