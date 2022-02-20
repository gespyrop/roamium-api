from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import pandas as pd

from .models import Place, Category
from .serializers import PlaceSerializer, PlaceDistanceSerializer, CategorySerializer
from .overpass import QueryBuilder
from .services.recommendation import CosineSimilarityRecommendationService


class PlaceViewSet(viewsets.ModelViewSet):
    recommendation_service = CosineSimilarityRecommendationService()
    permission_classes = [permissions.IsAdminUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'nearby', 'recommend'):
            return [permissions.IsAuthenticated()]

        return super(PlaceViewSet, self).get_permissions()

    def _parse_parameters(self, request) -> tuple:
        '''Parse the request's parameters.'''
        # Get user location parameters
        longitude = float(request.query_params.get('longitude'))
        latitude = float(request.query_params.get('latitude'))

        # Get radius        
        radius = float(request.query_params.get('radius', 1000))

        return longitude, latitude, radius

    def _get_places(self, request) -> list:
        '''Get places within the given radius from the given set of coordinates.'''
        longitude, latitude, radius = self._parse_parameters(request)
        user_location = Point(longitude, latitude, srid=4326)

        places = Place.objects.annotate(
            distance=Distance('location', user_location)
        ).filter(distance__lt=radius)

        builder = QueryBuilder(longitude, latitude, radius=radius)
        builder.add_node(name=None, amenity=None)
        osm_places = builder.run_query()

        return PlaceDistanceSerializer(places, many=True, context={'request': request}).data + osm_places

    @action(detail=False, methods=['GET'])
    def nearby(self, request):
        try:
            places = self._get_places(request)
        except TypeError:
            return Response({'message': "Float parameters 'longitude' and 'latitude' are required."}, 400)
        except ValueError:
            return Response({'message': "Parameters 'longitude' and 'latitude' must be of type 'float'."}, 400)

        # Sort all places by distance
        if len(places) > 0:
            places = pd.DataFrame(places).sort_values(by='distance').to_dict('records')

        return Response(places)
    
    @action(detail=False, methods=['GET'])
    def recommend(self, request):
        try:
            places = self._get_places(request)
        except TypeError:
            return Response({'message': "Float parameters 'longitude' and 'latitude' are required."}, 400)
        except ValueError:
            return Response({'message': "Parameters 'longitude' and 'latitude' must be of type 'float'."}, 400)

        # Recommend places
        recommendations = self.recommendation_service.recommend(places, request.data)

        return Response(recommendations)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]

        return super(CategoryViewSet, self).get_permissions()
