from django.urls import path
from . import views

app_name = 'weather4u'

urlpatterns = [
    path("", views.home, name="index"),
]