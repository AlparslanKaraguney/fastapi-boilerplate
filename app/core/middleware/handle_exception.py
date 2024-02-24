from starlette.middleware.base import BaseHTTPMiddleware
from app.core import custom_exceptions
from app.core.schema.response import ErrorResponse
from app.logs.log_handler import LibLogger
from fastapi import status, Request

log = LibLogger()


class BaseExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except custom_exceptions.CustomException as e:
            log.error(e)
            return ErrorResponse(e.status_code, str(e))
        except custom_exceptions.ValidationError as e:
            log.error(e)
            return ErrorResponse(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))
        except (
            custom_exceptions.AuthenticationFailedError,
            custom_exceptions.PermissionDeniedException,
        ) as e:
            log.error(e)
            return ErrorResponse(status.HTTP_401_UNAUTHORIZED, str(e))
        except Exception as e:
            log.error(e)
            return ErrorResponse(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "internal server error"
            )
