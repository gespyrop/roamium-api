from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Place, OSMPlace, Category


@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'location_display')
    default_lat = 37.9838
    default_lon = 23.7275
    default_zoom = 3

    def location_display(self, obj):
        return f'({obj.location.x}, {obj.location.y})'

    location_display.short_description = 'Location'


admin.site.register(OSMPlace)
admin.site.register(Category)
