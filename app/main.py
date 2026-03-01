from fastapi import FastAPI,Request,Response
import time
from app.models import *
from app.middlewares import TimeCounterMiddleware,RateTimeLimitMiddleware


from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter




from app.routers import posts_router
from app.routers import tags_router
from app.routers import category_router
from app.routers import proffesion_router
from app.routers import post_tag_router
from app.routers import user_router
from app.routers import comment_router
from app.routers import user_search_router
from app.routers import weather_router
from app.routers import auth_router
from app.routers import lesson_router
from app.schemas import zero_division_error,anasbek_slepp_error_exc,AnasbekSleepingException,rate_time_limet_error_exc,RateTimeLimetException
from app.admin import admin 
app = FastAPI(
    title="Chesnokdan achiq haqiqatlar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(category_router)
app.include_router(proffesion_router)
app.include_router(post_tag_router)
app.include_router(user_router)
app.include_router(comment_router)
app.include_router(user_search_router)
app.include_router(weather_router)
app.include_router(lesson_router)

app.add_exception_handler(ZeroDivisionError,zero_division_error)
app.add_exception_handler(AnasbekSleepingException,anasbek_slepp_error_exc)
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_exception_handler(RateTimeLimetException,rate_time_limet_error_exc)

app.add_middleware(middleware_class=TrustedHostMiddleware,allowed_hosts=["*"])
#DisallowedHost

app.add_middleware(middleware_class=CORSMiddleware,    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.add_middleware(middleware_class=TimeCounterMiddleware)
app.add_middleware(RateTimeLimitMiddleware)
admin.mount_to(app=app)
app.state.limiter=limiter