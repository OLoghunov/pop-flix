from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class PopFlixException(Exception):
    """This is the base class for all pop-flix errors"""

    pass


class InvalidToken(PopFlixException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(PopFlixException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(PopFlixException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(PopFlixException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(PopFlixException):
    """User has provided an email for a user who exists during sign up"""

    pass


class InvalidCredentials(PopFlixException):
    """User has provided wrong email or password during log in"""

    pass


class InsufficientPermission(PopFlixException):
    """User does not have the neccessary permissions to perform an action"""

    pass


class FilmNotFound(PopFlixException):
    """Film Not found"""

    pass



class UserNotFound(PopFlixException):
    """User Not found"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""

    pass


def createExceptionHandler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exceptionHandler(request: Request, exc: PopFlixException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exceptionHandler


def registerAllErrors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        createExceptionHandler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        createExceptionHandler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        FilmNotFound,
        createExceptionHandler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Film not found",
                "error_code": "film_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        createExceptionHandler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        createExceptionHandler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        createExceptionHandler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        createExceptionHandler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        createExceptionHandler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        createExceptionHandler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        FilmNotFound,
        createExceptionHandler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Film Not Found",
                "error_code": "film_not_found",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        createExceptionHandler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops... Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))
        
        return JSONResponse(
            content={
                "message": "Oops... Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
