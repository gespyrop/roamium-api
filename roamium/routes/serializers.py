from rest_framework import serializers
from .models import Route, Visit, Review


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ('user', 'finished', 'visits')

    def get_visits(self, obj):
        return VisitSerializer(
            obj.visit_set.all(), many=True, read_only=True
        ).data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
