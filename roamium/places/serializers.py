from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from .models import Place, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(read_only=True, child=serializers.CharField())
    location = PointField()
    class Meta:
        model = Place
        fields = '__all__'



class PlaceDistanceSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(read_only=True, child=serializers.CharField())
    distance = serializers.SerializerMethodField()
    location = PointField()

    def get_distance(self, obj):
        return obj.distance.m

    class Meta:
        model = Place
        fields = '__all__'