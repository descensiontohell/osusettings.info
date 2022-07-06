import json
import logging
import typing
from datetime import datetime

from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPException, HTTPNotImplemented, HTTPUnauthorized, \
    HTTPFound
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from backend.app.web.response import error_json_response

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    request.player_name = session.get("player_name")
    request.player_id = session.get("player_id")
    request.is_superuser = session.get("is_superuser")
    request.is_admin = session.get("is_admin")
    return await handler(request)


@middleware
async def response_time_middleware(request: "Request", handler: callable):
    start_time = datetime.now()
    try:
        response = await handler(request)
        return response
    finally:
        consumed_time = (datetime.now() - start_time).microseconds / 1000
        logger = logging.getLogger("REQUEST")
        logger.info(msg=consumed_time)


HTTP_ERROR_CODES = {
    302: "http found",
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPFound as e:
        raise HTTPFound(location=e.location)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=e.reason,
            data=e.text,
        )
    except HTTPNotImplemented as e:
        return error_json_response(
            http_status=405,
            status="not_implemented",
            message=e.reason,
            data=e.text,
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
    app.middlewares.append(response_time_middleware)
