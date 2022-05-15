from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from django.db.models import Avg

from .models import Place, Category
from routes.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    location = PointField()
    categories = serializers.ListSerializer(
        read_only=True,
        child=serializers.CharField()
    )

    def __init__(self, *args, **kwargs):
        self.place_source = kwargs.pop('source', 'roamium')
        super().__init__(*args, **kwargs)

    def get_source(self, obj):
        return self.place_source

    def get_rating(self, obj):
        return list(Review.objects.filter(
            visit__place_source=self.place_source,
            visit__place_id=obj.id
        ).aggregate(Avg('stars')).values())[0]

    class Meta:
        model = Place
        fields = '__all__'


class PlaceDistanceSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    location = PointField()
    categories = serializers.ListSerializer(
        read_only=True,
        child=serializers.CharField()
    )

    def __init__(self, *args, **kwargs):
        self.place_source = kwargs.pop('source', 'roamium')
        super().__init__(*args, **kwargs)

    def get_source(self, obj):
        return self.place_source

    def get_rating(self, obj):
        return list(Review.objects.filter(
            visit__place_source=self.place_source,
            visit__place_id=obj.id
        ).aggregate(Avg('stars')).values())[0]

    def get_distance(self, obj):
        return obj.distance.m

    class Meta:
        model = Place
        fields = '__all__'
