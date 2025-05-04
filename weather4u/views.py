import datetime
from urllib import request

import requests
import pytz
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from .models import ClothingItem



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

def what_to_wear(request):
    zipcode = request.GET.get("zipcode")
    result = get_weather_data(zipcode) if zipcode else None

    clothing = {
        "today": [],
        "next_5_days": []
    }

    if result:
        weather = result["weather"]
        local_timezone = pytz.timezone(result["timezone"])

        temp = weather["current"]["temp"]
        clothing["today"] = get_model_clothing_recommendations(temp)

        # Next 5 days
        for day in weather["daily"][:5]:
            dt = datetime.datetime.fromtimestamp(day["dt"], tz=local_timezone)
            avg_temp = (day["temp"]["max"] + day["temp"]["min"]) / 2
            icon = day["weather"][0]["icon"]
            desc = day["weather"][0]["description"]


            outfit = get_model_clothing_recommendations(avg_temp)

            clothing["next_5_days"].append({
                "name": dt.strftime("%A"),
                "temp_min": round(day["temp"]["min"]),
                "temp_max": round(day["temp"]["max"]),
                "description": desc.capitalize(),
                "icon": icon,
                "outfit": outfit
            })

    return render(request, "weather4u/what_to_wear.html", {"result": result, "clothing": clothing})



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

    next_5_days = []
    for day in weather_data["daily"][:5]:
        dt = datetime.datetime.fromtimestamp(day["dt"], tz=local_timezone)
        next_5_days.append({
            "name": dt.strftime("%A"),
            "temp_min": round(day["temp"]["min"]),
            "temp_max": round(day["temp"]["max"]),
            "description": day["weather"][0]["description"].capitalize(),
            "icon": day["weather"][0]["icon"],
        })

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
        "next_5_days": next_5_days,
        "timezone": timezone_name,
    }

    cache.set(cache_key, result, timeout=1300)
    return result

def get_model_clothing_recommendations(temp):
    categories = []

    if temp >= 85:
        categories.append("hot")
    elif temp >= 70:
        categories.append("warm")
    elif temp >= 55:
        categories.append("cool")
    else:
        categories.append("cold")

    return ClothingItem.objects.filter(categories__name__in=categories).distinct()

