import datetime
from urllib import request

import requests
import pytz
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache


def home(request):
    return render(request, 'weather4u/index.html')


def weather(request):
    zipcode = request.GET.get('zipcode')
    result = get_weather_data(zipcode) if zipcode else None
    return render(request, "weather4u/weather.html", {"result": result})

def five_day(request):
    zipcode = request.GET.get('zipcode')
    result = get_weather_data(zipcode) if zipcode else None
    return render(request, "weather4u/five_day.html", {"result": result})


def get_weather_data(zipcode):
    API_KEY = settings.API_KEY
    cache_key = f"weather:{zipcode}"
    result = cache.get(cache_key)

    if result:
        print(f"[Cache HIT] Using cached data for ZIP {zipcode}")
        return result

    print(f"[Cache MISS] Fetching data for ZIP {zipcode}")
    geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zipcode},US&appid={API_KEY}"
    geo_response = requests.get(geo_url)

    if geo_response.status_code != 200:
        return {"error": "Could not retrieve location for that ZIP code."}

    city_data = geo_response.json()
    lat = city_data["lat"]
    lon = city_data["lon"]

    weather_url = (
        f"https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
    )
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return {"error": "Could not retrieve weather data."}

    weather_data = weather_response.json()
    timezone_name = weather_data.get("timezone", "UTC")
    local_timezone = pytz.timezone(timezone_name)

    current_dt = datetime.datetime.fromtimestamp(weather_data["current"]["dt"], tz=local_timezone)
    day_str = current_dt.strftime("%a")

    now = datetime.datetime.now(tz=local_timezone)
    next_12_hours = []
    for hour in weather_data["hourly"]:
        hour_dt = datetime.datetime.fromtimestamp(hour["dt"], tz=local_timezone)
        if hour_dt > now:
            time = hour_dt.strftime("%I %p").lstrip("0")
            next_12_hours.append({
                "time": time,
                "temp": round(hour["temp"]),
                "description": hour["weather"][0]["description"].capitalize(),
                "icon": hour["weather"][0]["icon"],
            })
        if len(next_12_hours) == 12:
            break

    result = {
        "zipcode": zipcode,
        "city": city_data.get("name", "Unknown"),
        "state": city_data.get("state", ""),
        "country": city_data.get("country", ""),
        "lat": lat,
        "lon": lon,
        "weather": weather_data,
        "icon": weather_data["current"]["weather"][0]["icon"],
        "day": day_str,
        "next_12_hours": next_12_hours,
        "timezone": timezone_name,
    }

    cache.set(cache_key, result, timeout=1300)
    return result
