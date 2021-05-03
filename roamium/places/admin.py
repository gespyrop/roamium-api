from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Place, Category

@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'time')
    default_lat = 37.9838
    default_lon = 23.7275
    default_zoom = 3

admin.site.register(Category)