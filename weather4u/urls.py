from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'weather4u'

urlpatterns = [
    path("", views.home, name="index"),
    path("weather/", views.weather, name="weather"),
    path('five-day/', views.five_day, name='five_day'),
    path("what-to-wear/", views.what_to_wear, name="what_to_wear"),

    path("what-to-do/", views.what_to_do, name="what_to_do"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="weather4u/login.html",
        redirect_authenticated_user=True,
        next_page='weather4u:index'
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="weather4u:index"), name="logout"),
]
