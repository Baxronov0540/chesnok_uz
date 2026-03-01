from fastapi import Request

from slowapi import Limiter
from slowapi.util import get_remote_address


def get_global_key(requset:Request):

    return "global_rate_limet"

limiter=Limiter(key_func=get_remote_address)
