from django.urls import path
from . import views

app_name = 'weather4u'

urlpatterns = [
    path("", views.home, name="index"),
    path("weather/", views.weather, name="weather"),
    path('five-day/', views.five_day, name='five_day'),
    path("what-to-wear/", views.what_to_wear, name="what_to_wear"),
]
