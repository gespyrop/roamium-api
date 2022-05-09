import requests
from django.contrib.gis.geos import Point

from .serializers import PlaceSerializer
from .models import Place, OSMPlace

KEYWORD_TAGS = (
    'amenity', 'shop', 'cuisine', 'alcohol',
    'leisure', 'club', 'historic', 'tourism'
)

EXCLUDED_AMENITIES = (
    'fuel', 'pharmacy', 'driving_school', 'kindergarten', 'veterinary',
    'clinic', 'bus_station', 'school', 'bank', 'post_office', 'car_wash',
    'courthouse', 'bureau_de_change', 'taxi', 'doctors', 'police'
)


class QueryBuilder:

    def __init__(self, longitude, latitude, radius=1000):
        self.longitude = longitude
        self.latitude = latitude
        self.user_location = Point(self.longitude, self.latitude, srid=4326)
        self.radius = radius
        self.query_elements = [
            '[out:json];(',
            ');out;'
        ]

    def add_node(self, **kwargs):
        node = 'node'
        for key, value in kwargs.items():
            node += f'[{key}={value}]' if value else f'[{key}]'

        # Exclude specific types of amenities
        excluded = '|'.join(EXCLUDED_AMENITIES)
        node += f'[amenity!~"{excluded}"]'

        node += f'(around: {self.radius}, {self.latitude}, {self.longitude});'
        self.query_elements.insert(-1, node)

    def add_node_by_id(self, id):
        self.query_elements.insert(-1, f'node({id});')

    @property
    def query(self):
        return ''.join(self.query_elements)

    def run_query(self):
        response = requests.post(
            'https://overpass-api.de/api/interpreter',
            data={'data': self.query}
        )
        data = response.json()

        places = []

        for element in data['elements']:
            place_id = element['id']
            location = Point(element['lon'], element['lat'], srid=4326)

            tags = element.get('tags', {})
            name = tags.get('name', '')
            wheelchair = tags.get('wheelchair')

            # Get mirrored local place for additional information
            place = PlaceSerializer(
                Place(
                    id=place_id, name=name,
                    location=location, wheelchair=wheelchair
                ),
                source='osm'
            ).data

            place['distance'] = self.user_location.distance(location) * 100000

            try:
                osm_place = OSMPlace.objects.get(osm_id=place_id)

                # Overwrite existing data
                if osm_place.name:
                    place['name'] = osm_place.name

                if osm_place.wheelchair:
                    place['wheelchair'] = osm_place.wheelchair

                place['categories'] = [
                    str(category) for category in osm_place.categories.all()
                ]

            except OSMPlace.DoesNotExist:
                place['categories'] = []

            # Extract categories from tags
            for label in KEYWORD_TAGS:
                if label in tags:
                    # Multiple values are separated with ';'
                    place['categories'] += tags[label].split(';')

            places.append(place)

        return places
