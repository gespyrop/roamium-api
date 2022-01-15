import requests
from django.contrib.gis.geos import Point

from .serializers import PlaceSerializer
from .models import Place


class QueryBuilder:

    def __init__(self):
        self.query_elements = [
            '[out:json];(',
            ');out;'
        ]
    
    def add_node(self, lat, lon, radius=1000, **kwargs):
        node = 'node'
        for key, value in kwargs.items():
            node += f'[{key}={value}]' if value else f'[{key}]'

        node += f'(around: {radius}, {lat}, {lon});'
        self.query_elements.insert(-1, node)
    
    @property
    def query(self):
        return ''.join(self.query_elements)

    def run_query(self):
        response = requests.post('https://overpass-api.de/api/interpreter', data={'data': self.query})
        data = response.json()

        places = []
        
        for element in data['elements']:
            place_id = element['id']
            location = Point(element['lat'], element['lon'])

            tags = element.get('tags', {})

            name = tags.get('name', '')
            wheelchair = tags.get('wheelchair', 'no')

            place = PlaceSerializer(Place(id=place_id, name=name, location=location, wheelchair=wheelchair)).data

            # Extract categories from tags
            data['categories'] = []

            for label in ('amenity', 'shop'):
                if label in tags:
                    place['categories'].append(tags[label])

            places.append(place)

        return places
