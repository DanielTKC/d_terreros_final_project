from django.contrib import admin
from .models import ClothingItem, ClothingCategory

admin.site.register(ClothingItem)
admin.site.register(ClothingCategory)
