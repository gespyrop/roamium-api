from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import pandas as pd

from .models import Place, Category
from .serializers import PlaceSerializer, PlaceDistanceSerializer, CategorySerializer
from .overpass import QueryBuilder

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
        except ValueError:
            return Response({'message': "Parameters 'latitude' and 'longitude' must be of type 'float'."}, 400)

        # Sort places by their distance from the user's location
        user_location = Point(longitude, latitude, srid=4326)

        places = Place.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance')

        builder = QueryBuilder(longitude, latitude, radius=2000)
        builder.add_node(name=None, amenity=None)
        osm_places = builder.run_query()

        all_places = PlaceDistanceSerializer(places, many=True, context={'request': request}).data + osm_places

        # Sort all places by distance
        all_places = pd.DataFrame(all_places).sort_values(by='distance').to_dict('records')

        return Response(all_places)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]

        return super(CategoryViewSet, self).get_permissions()
