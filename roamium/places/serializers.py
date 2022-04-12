from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from .models import Place, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    categories = serializers.ListSerializer(read_only=True, child=serializers.CharField())
    location = PointField()

    def __init__(self, *args, **kwargs):
        self.place_source = kwargs.pop('source', 'roamium')
        super().__init__(*args, **kwargs)
    
    def get_source(self, obj):
        return self.place_source

    class Meta:
        model = Place
        fields = '__all__'



class PlaceDistanceSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    categories = serializers.ListSerializer(read_only=True, child=serializers.CharField())
    distance = serializers.SerializerMethodField()
    location = PointField()

    def __init__(self, *args, **kwargs): 
        self.place_source = kwargs.pop('source', 'roamium')
        super().__init__(*args, **kwargs)
    
    def get_source(self, obj):
        return self.place_source

    def get_distance(self, obj):
        return obj.distance.m

    class Meta:
        model = Place
        fields = '__all__'