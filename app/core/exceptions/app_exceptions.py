from typing import Union

from fastapi import HTTPException, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, error_message, context=None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.error_message = error_message
        self.context = context
        if self.context:
            logger.critical(self.context)
        else:
            if self.error_message:
                logger.error(self.error_message)

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - error_message = {self.error_message}"
        )


def app_exception_handler(exc):
    if isinstance(exc, PyMongoError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "app_exception": "Database Error",
                "errorMessage": exc.args,
            },
            media_type="application/json",
        )
    if isinstance(exc, HTTPException):
        return JSONResponse(
            content={"app_exception": "HTTP Error", "errorMessage": exc.detail},
            status_code=exc.status_code,
            media_type="application/json",
        )
    return JSONResponse(
        content={
            "app_exception": exc.exception_case,
            "errorMessage": exc.error_message,
        },
        status_code=exc.status_code,
        media_type="application/json",
    )


class AppException:
    class OperationError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, error_message, context=None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class InternalServerError(AppExceptionCase):
        """
        Generic Exception to catch failed operations
        """

        def __init__(self, error_message, context=None):
            status_code = 500
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class ResourceExists(AppExceptionCase):
        """
        Resource Creation Failed Exception
        """

        def __init__(self, error_message, context=None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class NotFoundException(AppExceptionCase):
        def __init__(self, error_message: Union[str, None], context=None):
            """
            Resource Not Found Exception
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class Unauthorized(AppExceptionCase):
        def __init__(self, error_message, context=None):
            """
            Unauthorized Exception
            :param error_message:
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class ValidationException(AppExceptionCase):
        """
        Resource Validation Exception
        """

        def __init__(self, error_message, context=None):
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class BadRequest(AppExceptionCase):
        def __init__(self, error_message, context=None):
            """
            Bad Request

            :param error_message:
            """
            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class ExpiredTokenException(AppExceptionCase):
        def __init__(self, error_message, context=None):
            """
            Expired Token Exception
            :param error_message:
            """

            status_code = 400
            AppExceptionCase.__init__(self, status_code, error_message, context=context)

    class ServiceRequestException(AppExceptionCase):
        def __init__(self, error_message, context=None):
            """
            External Service Request Exception
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, error_message, context=context)
