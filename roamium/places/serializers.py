from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    location = PointField()
    class Meta:
        model = Place
        fields = '__all__'
