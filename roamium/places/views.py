from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Place
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'nearby'):
            return [permissions.IsAuthenticated()]

        return super(PlaceViewSet, self).get_permissions()
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        # Get user location parameters
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
        except TypeError:
            return Response({'message': "Float parameters 'latitude' and 'longitude' are required."}, 400)
        
        # Get limit parameter
        try:
            limit = int(request.query_params.get('limit')) if 'limit' in request.query_params else 20
        except TypeError:
            return Response({'message': "The limit parameter must be an integer."}, 400)

        # Sort places by their distance from the user's location
        user_location = Point(latitude, longitude, srid=4326)

        places = Place.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')[:limit]

        return Response(PlaceSerializer(places, many=True, context={'request': request}).data)
