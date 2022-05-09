import json
import requests
from abc import ABC, abstractmethod


class DirectionsService(ABC):
    '''Handles direction provision.'''

    @abstractmethod
    def get_directions(self, points: list, profile: str) -> tuple:
        '''
        Provides a directions and summary information for the
        best route that passes through the provided set of points.
        '''
        pass


class ORSDirectionsService(DirectionsService):
    '''Handles direction provision by calling the [Open Route Service](https://openrouteservice.org/).'''

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openrouteservice.org/v2'
    
    def get_directions(self, points: list, profile: str = 'foot-walking') -> tuple:
        '''
        Provides a directions and summary information for the
        best route that passes through the provided set of points.
        '''
        endpoint = f'/directions/{profile}'

        payload = json.dumps({
            'coordinates': points,
            'instructions': False,
            'units': 'km'
        })

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(f'{self.base_url}{endpoint}', data=payload, headers=headers)

        route = response.json()['routes'][0]

        return route['geometry'], route['summary']['distance'], route['summary']['duration']
