import time
from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import  BaseHTTPMiddleware

from app.schemas import RateTimeLimetException

class TimeCounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        start_time=time.perf_counter()

        response=await call_next(request)
        
        procces_time=time.perf_counter()-start_time
        response.headers["X-Procces-Time"]=str(procces_time)

        return response

d = {}

class RateTimeLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        user_ip = request.client.host
        now = time.time()

        if user_ip not in d:
            d[user_ip] = [1, now]  
        else:
            count, start = d[user_ip]

            if now - start > 120:
                d[user_ip] = [1, now]
            else:
                if count >= 5:
                    raise RateTimeLimetException("2 minda 5 ta urinishga huquq bor sizda !!")
                d[user_ip][0] += 1

        response = await call_next(request)
        return response
