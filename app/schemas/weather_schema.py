from pydantic import BaseModel


class WeatherCord(BaseModel):
    lon: float
    lat: float


class WeatherInline(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMain(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float
    sea_level: float
    grnd_level: float


class WeatherWind(BaseModel):
    speed: float
    deg: float
    gust: float


class WeatherClouds(BaseModel):
    all: int


class WeatherSys(BaseModel):
    country: str
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    coord: WeatherCord
    weather: list[WeatherInline]
    base: str
    # main:WeatherMain
    # visibility:int
    # wind:WeatherWind
    # clouds:WeatherClouds
    # dt:int
    # sys:WeatherSys
    # timezone:int
    # id:int
    # name:str
    # cod:int
