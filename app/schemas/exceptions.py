from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError ,ResponseValidationError
from fastapi import status




class AnasbekSleepingException(Exception):

    def __init__(self,msg):
        self.msg=msg


async def anasbek_slepp_error_exc(request:Request,exc:AnasbekSleepingException):

    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE
        ,content={
            "message":exc.msg
        }
    )




class RateTimeLimetException(Exception):
    def __init__(self,msg):
        self.msg=msg

async def rate_time_limet_error_exc(request:Request,exc:RateTimeLimetException):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"message":exc.msg}
    )        






async def zero_division_error(
        request:Request,
        exc:ZeroDivisionError,
        ):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message":exc.args[0]
        }
    )
