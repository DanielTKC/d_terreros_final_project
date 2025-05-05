import datetime
import requests
import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache import cache
from .models import ClothingItem
from .models import Activity



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("weather4u:index")
    else:
        form = UserCreationForm()
    return render(request, "weather4u/register.html", {"form": form})

def home(request):
    return render(request, 'weather4u/index.html')

@login_required
def profile(request):
    return render(request, "weather4u/profile.html")


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
        condition = weather["current"]["weather"][0]["main"].lower()
        local_timezone = pytz.timezone(result["timezone"])
        uvi = weather["current"].get("uvi", 0)


        temp = weather["current"]["temp"]
        clothing["today"] = get_model_clothing_recommendations(temp, condition, uvi)

        # Next 5 days
        for day in weather["daily"][:5]:
            dt = datetime.datetime.fromtimestamp(day["dt"], tz=local_timezone)
            avg_temp = (day["temp"]["max"] + day["temp"]["min"]) / 1.5
            icon = day["weather"][0]["icon"]
            desc = day["weather"][0]["description"]


            outfit = get_model_clothing_recommendations(avg_temp, condition, uvi)

            clothing["next_5_days"].append({
                "name": dt.strftime("%A"),
                "temp_min": round(day["temp"]["min"]),
                "temp_max": round(day["temp"]["max"]),
                "description": desc.capitalize(),
                "icon": icon,
                "outfit": outfit
            })

    return render(request, "weather4u/what_to_wear.html", {"result": result, "clothing": clothing})

def what_to_do(request):
    zipcode = request.GET.get("zipcode")
    result = get_weather_data(zipcode) if zipcode else None

    activities = {
        "today": [],
        "next_5_days": []
    }

    if result:
        weather = result["weather"]
        local_timezone = pytz.timezone(result["timezone"])

        temp = weather["current"]["temp"]
        condition = weather["current"]["weather"][0]["main"]
        activities["today"] = get_activity_recommendations(temp, condition)

        for day in weather["daily"][:5]:
            dt = datetime.datetime.fromtimestamp(day["dt"], tz=local_timezone)
            avg_temp = (day["temp"]["max"] + day["temp"]["min"]) / 2
            condition = day["weather"][0]["main"]
            icon = day["weather"][0]["icon"]
            desc = day["weather"][0]["description"]

            recs = get_activity_recommendations(avg_temp, condition)

            activities["next_5_days"].append({
                "name": dt.strftime("%A"),
                "temp_min": round(day["temp"]["min"]),
                "temp_max": round(day["temp"]["max"]),
                "description": desc.capitalize(),
                "icon": icon,
                "recs": recs,
            })

    return render(request, "weather4u/what_to_do.html", {"result": result, "activities": activities})



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

def get_model_clothing_recommendations(temp, condition, uvi):

    categories = []

    if temp >= 85:
        categories.append("hot")
    elif temp >= 75:
        categories.append("warm")
    elif temp >= 55:
        categories.append("cool")
    else:
        categories.append("cold")

    if "rain" in condition:
        categories.append("rain")
    if "snow" in condition:
        categories.append("snow")
    if uvi >= 6:
        categories.append("uv_high")

    return ClothingItem.objects.filter(categories__name__in=categories).distinct()

def get_activity_recommendations(temp, condition):
    condition = condition.lower()

    if "snow" in condition:
        category_name = "snow"
    elif "light rain" in condition:
        category_name = "light_rain"
    elif "rain" in condition:
        category_name = "rain"
    elif any(word in condition for word in ["clear", "clouds", "sun"]):
        category_name = "sunny"
    else:
        category_name = None

    if not category_name:
        return []

    activities = Activity.objects.filter(categories__name=category_name)
    matching = []
    for activity in activities:
        # print(activity.name, activity.min_temp, activity.max_temp)

        if activity.min_temp - 10 <= temp <= activity.max_temp:
            matching.append(activity)

    return matching

