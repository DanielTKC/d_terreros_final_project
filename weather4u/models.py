from django.db import models

class ClothingCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ClothingItem(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='clothing_icons/', blank=True, null=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ClothingCategory, related_name="clothing_items")

    def __str__(self):
        return self.name

class ActivityCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_temp = models.IntegerField()
    max_temp = models.IntegerField()
    categories = models.ManyToManyField(ActivityCategory, related_name="activities")

    def __str__(self):
        return self.name