from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from unittest.mock import patch

from places.models import Place
from shared.test_utils import create_test_user, create_test_superuser, \
    create_test_place, create_test_category, place_payload
import json

PLACES_URL = reverse('place-list')

CONTENT_TYPE = 'application/json'
UPDATED_NAME = 'New Test Name'


class PlaceApiTest(TestCase):
    '''Tests for the Place endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = place_payload.copy()

    def authenticateAdmin(self):
        admin = create_test_superuser()
        self.client.force_authenticate(admin)

    def authenticateRegularUser(self):
        user = create_test_user()
        self.client.force_authenticate(user)

    def setUp(self):
        self.client = APIClient()

    def test_create_place_admin_user(self):
        '''Test that admin users can create places'''
        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.post(
            PLACES_URL, json.dumps(self.payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Check that the place was created successfuly
        place = Place.objects.get(name=self.payload['name'])
        self.assertEquals(place.name, self.payload['name'])

    def test_create_place_regular_user(self):
        '''Test that regular users can not create places'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.post(
            PLACES_URL, json.dumps(self.payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was not created
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=self.payload['name'])

    def test_create_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not create places'''
        response = self.client.post(
            PLACES_URL, json.dumps(self.payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_list_places_authenticated_user(self):
        '''Test that authenticated users can list places'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create 3 places
        for _ in range(3):
            create_test_place()

        response = self.client.get(PLACES_URL)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that 3 places were returned
        self.assertEquals(len(response.data), 3)

    def test_list_places_unauthenticated_user(self):
        '''Test that unauthenticated users can not list places'''
        # Create 3 places
        for _ in range(3):
            create_test_place()

        response = self.client.get(PLACES_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_retrieve_place_authenticated_user(self):
        '''Test that authenticated users can retrieve places'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create a place
        place = create_test_place()

        response = self.client.get(reverse('place-detail', args=(place.id,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the correct place was returned
        self.assertEquals(response.data['id'], place.id)

    def test_retrieve_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve places'''
        # Create a place
        place = create_test_place()

        response = self.client.get(reverse('place-detail', args=(place.id,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_update_place_admin_user(self):
        '''Test that admin users can update places'''
        # Create a test place
        place = create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        payload = self.payload.copy()
        payload['name'] = UPDATED_NAME

        response = self.client.put(
            reverse('place-detail', args=(place.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the place was updated successfuly
        place = Place.objects.get(name=payload['name'])
        self.assertEquals(place.name, payload['name'])

    def test_update_place_regular_user(self):
        '''Test that regular users can not update places'''
        # Create a place
        place = create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        payload = self.payload.copy()
        payload['name'] = UPDATED_NAME

        response = self.client.put(
            reverse('place-detail', args=(place.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was not updated
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=payload['name'])

    def test_update_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not update places'''
        # Create a test place
        place = create_test_place()

        payload = self.payload.copy()
        payload['name'] = UPDATED_NAME

        response = self.client.put(
            reverse('place-detail', args=(place.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_partial_update_place_admin_user(self):
        '''Test that admin users can partially update places'''
        # Create a test place
        place = create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.patch(
            reverse('place-detail', args=(place.id,)),
            json.dumps({'name': 'NewName'}),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the place was updated successfuly
        place = Place.objects.get(name='NewName')
        self.assertEquals(place.name, 'NewName')

    def test_partial_update_place_regular_user(self):
        '''Test that regular users can not partially update places'''
        # Create a place
        place = create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.patch(
            reverse('place-detail', args=(place.id,)),
            {'name': 'NewName'},
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was created successfuly
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name='NewName')

    def test_partial_update_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not partially update places'''
        # Create a test place
        place = create_test_place()

        response = self.client.patch(
            reverse('place-detail', args=(place.id,)),
            {'name': 'NewName'},
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_place_admin_user(self):
        '''Test that admin users can destroy places'''
        # Create a test place
        place = create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.delete(
            reverse('place-detail', args=(place.id,))
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 204)

    def test_destroy_place_regular_user(self):
        '''Test that regular users can not destroy places'''
        # Create a place
        place = create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.delete(
            reverse('place-detail', args=(place.id,))
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

    def test_destroy_unauthenticated_user(self):
        '''Test that unauthenticated users can not destroy places'''
        # Create a test place
        place = create_test_place()

        response = self.client.delete(
            reverse('place-detail', args=(place.id,))
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    @patch('places.overpass.QueryBuilder.run_query', return_value=[])
    def test_nearby_places_authenticated_user(self, *args):
        '''Test that authenticated users can fetch nearby places'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create 3 places
        create_test_place(location={'latitude': 1.0, 'longitude': 1.0})
        closest_place = create_test_place(
            location={'latitude': 0.001, 'longitude': 0.001}
        )

        furthest_place = create_test_place(
            location={'latitude': 0.002, 'longitude': 0.002}
        )

        response = self.client.get(
            reverse('place-nearby'), data={'latitude': 0.0, 'longitude': 0.0}
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the places were returned in the correct order
        self.assertEquals(response.data[0].get('id'), closest_place.id)
        self.assertEquals(response.data[-1].get('id'), furthest_place.id)

    @patch('places.overpass.QueryBuilder.run_query', return_value=[])
    def test_nearby_places_unauthenticated_user(self, *args):
        '''Test that unauthenticated users can not fetch nearby places'''
        response = self.client.get(
            reverse('place-nearby'), data={'latitude': 0.0, 'longitude': 0.0}
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    @patch('places.overpass.QueryBuilder.run_query', return_value=[])
    def test_nearby_places_invalid_parameters(self, *args):
        '''
        Test that the "latitude" and "longitude" parameters
        are required for the nearby action
        '''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.get(reverse('place-nearby'))

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that an error message is returned
        self.assertEquals(
            response.data.get('message'),
            "Float parameters 'longitude' and 'latitude' are required."
        )

    def test_category_list(self):
        '''Test that a list of categories is included to the place payload'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create test place
        place = create_test_place()

        # Add 2 categories
        category_1 = create_test_category(name='Test 1')
        category_2 = create_test_category(name='Test 2')
        place.categories.add(category_1)
        place.categories.add(category_2)

        response = self.client.get(reverse('place-detail', args=(place.id,)))

        # Test that both categories were returned in a list
        self.assertIn(category_1.name, response.data['categories'])
        self.assertIn(category_2.name, response.data['categories'])

    @patch('places.overpass.QueryBuilder.run_query', return_value=[])
    def test_nearby_categories(self, *args):
        '''
        Test that all the categories of the places
        near the given location are collected.
        '''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create test places
        place1 = create_test_place(
            location={'latitude': 0.001, 'longitude': 0.001}
        )

        place2 = create_test_place(
            location={'latitude': 0.002, 'longitude': 0.002}
        )

        # Add 2 categories
        category_1 = create_test_category(name='Test 1')
        category_2 = create_test_category(name='Test 2')
        place1.categories.add(category_1)
        place1.categories.add(category_2)
        place2.categories.add(category_2)

        response = self.client.get(
            reverse('place-nearby-categories'),
            data={'latitude': 0.0, 'longitude': 0.0}
        )

        # Test that both categories were returned in a list
        self.assertIn(category_1.name, response.data)
        self.assertIn(category_2.name, response.data)
