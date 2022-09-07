from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import pandas as pd
import os

from .models import Place, Category
from .serializers import PlaceSerializer, PlaceDistanceSerializer,\
    CategorySerializer
from .overpass import QueryBuilder
from .services.recommendation import CosineSimilarityRecommendationService
from .services.directions import ORSDirectionsService

OSM_PLACE_TAGS = ('amenity', 'historic', 'tourism', 'shop')
ORS_API_KEY = os.environ.get('ORS_API_KEY')

LON_LAT_REQUIRED = "Float parameters 'longitude' and 'latitude' are required."
LON_LAT_FLOAT = "Parameters 'longitude' and 'latitude' must be 'float'."


class PlaceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action in (
            'list', 'retrieve', 'nearby',
            'nearby_categories', 'recommend', 'directions'
        ):
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

    def _get_places(self, request) -> tuple:
        '''
        Get places within the given radius
        from the given set of coordinates.
        '''
        longitude, latitude, radius = self._parse_parameters(request)
        user_location = Point(longitude, latitude, srid=4326)

        places = Place.objects.annotate(
            distance=Distance('location', user_location)
        ).filter(distance__lt=radius)

        # Instantiate a new QueryBuilder
        builder = QueryBuilder(longitude, latitude, radius=radius)

        # Add a node for every OSM tag
        for tag in OSM_PLACE_TAGS:
            builder.add_node(name=None, **{tag: None})

        # Run the query to fetch the places
        try:
            osm_places = builder.run_query()
        except ValueError:
            raise RuntimeError('Overpass rate limit!')

        return PlaceDistanceSerializer(
            places, many=True, context={'request': request}
        ).data + osm_places, radius

    @action(detail=False, methods=['GET'])
    def nearby(self, request):
        try:
            places, radius = self._get_places(request)
        except TypeError:
            return Response(
                {'detail': LON_LAT_REQUIRED},
                status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response(
                {'detail': LON_LAT_FLOAT},
                status.HTTP_400_BAD_REQUEST
            )
        except RuntimeError as e:
            return Response({'detail': str(e)}, status.HTTP_400_BAD_REQUEST)

        # Sort all places by distance
        if len(places) > 0:
            places = pd.DataFrame(places)\
                .sort_values(by='distance').to_dict('records')

        return Response(places)

    @action(detail=False, methods=['GET'], url_path='nearby/categories')
    def nearby_categories(self, request):
        try:
            places, radius = self._get_places(request)
        except TypeError:
            return Response(
                {'detail': LON_LAT_REQUIRED},
                status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response(
                {'detail': LON_LAT_FLOAT},
                status.HTTP_400_BAD_REQUEST
            )
        except RuntimeError as e:
            return Response({'detail': str(e)}, status.HTTP_400_BAD_REQUEST)

        # Use a set to collect all the discrete categories
        categories = set()
        for place in places:
            for category in place['categories']:
                categories.add(category)

        return Response(list(categories))

    @action(detail=False, methods=['POST'])
    def recommend(self, request):
        try:
            places, radius = self._get_places(request)
        except TypeError:
            return Response(
                {'detail': LON_LAT_REQUIRED},
                status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response(
                {'detail': LON_LAT_FLOAT},
                status.HTTP_400_BAD_REQUEST
            )
        except RuntimeError as e:
            return Response({'detail': str(e)}, status.HTTP_400_BAD_REQUEST)

        # Calculate wieghts
        categories_weight = 8
        wheelchair_weight = 2 * int(request.data.get('wheelchair', 0) > 0)
        distance_weight = 1
        rating_weight = 3

        weights = [
            categories_weight,
            wheelchair_weight,
            distance_weight,
            rating_weight
        ]

        # Recommend places
        recommendation_service = CosineSimilarityRecommendationService(
            weights=weights
        )

        recommendations = recommendation_service.recommend(
            places,
            request.data
        )

        return Response(recommendations)

    @action(detail=False, methods=['POST'])
    def directions(self, request):

        if 'points' not in request.data:
            return Response(
                {'detail': '"points" field is required.'},
                status.HTTP_400_BAD_REQUEST
            )

        profile = request.data.get('profile', 'foot-walking')
        points = request.data.get('points')

        if type(points) != list:
            return Response(
                {'detail': '"points" must be a list of coordinates.'},
                status.HTTP_400_BAD_REQUEST
            )

        directions_service = ORSDirectionsService(ORS_API_KEY)
        geometry, distance, duration = directions_service.get_directions(
            points,
            profile=profile
        )

        return Response({
            'geometry': geometry,
            'distance': distance,
            'duration': duration
        })


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]

        return super(CategoryViewSet, self).get_permissions()
