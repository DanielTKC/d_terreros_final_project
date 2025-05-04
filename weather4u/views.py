import datetime
import requests
from django.shortcuts import render

def home(request):
    return render(request, 'weather4u/index.html')

