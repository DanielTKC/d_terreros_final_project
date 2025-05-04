import datetime
import requests
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

def home(request):
    return render(request, 'weather4u/index.html')


def weather(request):
    API_KEY = settings.API_KEY
    zipcode = request.GET.get("zipcode")
    result = None

    if zipcode:
        # Cache it so we don't have to call the API every time
        cache_key = f"weather:{zipcode}"
        result = cache.get(cache_key)


        if not result:
            print(f"[Cache MISS] Fetching data for ZIP {zipcode}")

            geo_url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zipcode},US&appid={API_KEY}"
            geo_response = requests.get(geo_url)

            if geo_response.status_code == 200:
                city_data = geo_response.json()
                lat = city_data["lat"]
                lon = city_data["lon"]

                weather_url = (
                    f"https://api.openweathermap.org/data/3.0/onecall"
                    f"?lat={lat}&lon={lon}&units=imperial&appid={API_KEY}"
                )
                weather_response = requests.get(weather_url)

                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    result = {
                        "zipcode": zipcode,
                        "city": city_data.get("name", "Unknown"),
                        "state": city_data.get("state", ""),
                        "country": city_data.get("country", ""),
                        "lat": lat,
                        "lon": lon,
                        "weather": weather_data,
                    }
                    print(result)
                    cache.set(cache_key, result, timeout=1300)
                else:
                    weather_data = {"error": "Could not retrieve weather data."}
            else:
                print(f"[Cache HIT] Using cached data for ZIP {zipcode}")

                weather_data = {"error": "Could not retrieve location for that ZIP code."}

    return render(request, "weather4u/weather.html", {"result": result})
