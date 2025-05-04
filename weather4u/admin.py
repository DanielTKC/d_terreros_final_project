from django.contrib import admin
from .models import ClothingItem, ClothingCategory, Activity, ActivityCategory

@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("categories",)

@admin.register(ClothingCategory)
class ClothingCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "min_temp", "max_temp")
    search_fields = ("name",)
    filter_horizontal = ("categories",)

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
