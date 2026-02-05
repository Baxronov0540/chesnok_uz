from fastapi import APIRouter, HTTPException
import httpx
from enum import Enum

from app.schemas import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

API_KEY = "214d21e00f9b966bc4ade4ce7d85de22"


@router.get("/today/", response_model=WeatherResponse)
async def get_weather_today(city: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
            )
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return resp.json()


class WeatherType(str, Enum):
    toshkent = "Toshkent"
    samarqand = "Samarqand"
    navoi = "Navoi"
    buxoro = "Buxoro"
    namangan = "Namangan"
    andijon = "Andijon"
    fergana = "Farg'ona"
    sirdaryo = "Sirdaryo"
    surxondaryo = "Surxondaryo"
    qashqadaryo = "Qashqadaryo"
    xorazm = "Xorazm"
    qaraqalpogiston = "Qaraqalpog'iston"


@router.get("/Uzbekistan/today", response_model=WeatherResponse)
async def uzbek_weather(city: WeatherType):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=f"https://api.openweathermap.org/data/2.5/weather?q={city.value}&units=metric&appid={API_KEY}"
            )
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return resp.json()
