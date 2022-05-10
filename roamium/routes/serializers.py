from rest_framework import serializers
from .models import Route, Visit


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
