from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from places.models import Place
from shared.test_utils import create_test_user, create_test_superuser, create_test_place
import json

PLACES_URL = reverse('place-list')


class PlaceApiTest(TestCase):
    '''Tests for the Place endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = {
            'name': 'TestPlace',
            'location': {
                'latitude': 0.0,
                'longitude': 0.0
            },
            'time': '00:10:00',
            'is_bike': True,
            'is_wheelchair': True,
            'is_family': True,
            'is_friends': True,
        }
    
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

        response = self.client.post(PLACES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Check that the place was created successfuly
        place = Place.objects.get(name=self.payload['name'])
        self.assertEquals(place.name, self.payload['name'])
    
    def test_create_place_regular_user(self):
        '''Test that regular users can not create places'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.post(PLACES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was created successfuly
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=self.payload['name'])
    
    def test_create_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not create places'''
        response = self.client.post(PLACES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)
    
    def test_list_places_authenticated_user(self):
        '''Test that authenticated users can list places'''
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
        self.authenticateRegularUser()

        # Create a place
        create_test_place()

        response = self.client.get(reverse('place-detail', args=(1,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the correct place was returned
        self.assertEquals(response.data['id'], 1)

    def test_retrieve_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve places'''
        # Create a places
        create_test_place()

        response = self.client.get(reverse('place-detail', args=(1,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_update_place_admin_user(self):
        '''Test that admin users can update places'''
        # Create a test place
        create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('place-detail', args=(1,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the place was updated successfuly
        place = Place.objects.get(name=payload['name'])
        self.assertEquals(place.name, payload['name'])
    
    def test_update_place_regular_user(self):
        '''Test that regular users can not update places'''
        # Create a place 
        create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('place-detail', args=(1,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was created successfuly
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name=payload['name'])
    
    def test_update_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not update places'''
        # Create a test place
        create_test_place()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('place-detail', args=(1,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_partial_update_place_admin_user(self):
        '''Test that admin users can partially update places'''
        # Create a test place
        create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.patch(reverse('place-detail', args=(1,)), json.dumps({'name': 'NewName'}), content_type='application/json')

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the place was updated successfuly
        place = Place.objects.get(name='NewName')
        self.assertEquals(place.name, 'NewName')
    
    def test_partial_update_place_regular_user(self):
        '''Test that regular users can not partially update places'''
        # Create a place 
        create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.patch(reverse('place-detail', args=(1,)), {'name': 'NewName'}, content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the place was created successfuly
        with self.assertRaises(Place.DoesNotExist):
            Place.objects.get(name='NewName')
        
    def test_update_place_unauthenticated_user(self):
        '''Test that unauthenticated users can not partially update places'''
        # Create a test place
        create_test_place()

        response = self.client.patch(reverse('place-detail', args=(1,)), {'name': 'NewName'}, content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_place_admin_user(self):
        '''Test that admin users can destroy places'''
        # Create a test place
        create_test_place()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.delete(reverse('place-detail', args=(1,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 204)
    
    def test_destroy_place_regular_user(self):
        '''Test that regular users can not destroy places'''
        # Create a place 
        create_test_place()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.delete(reverse('place-detail', args=(1,)))

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)
        
    def test_destroy_unauthenticated_user(self):
        '''Test that unauthenticated users can not destroy places'''
        # Create a test place
        create_test_place()

        response = self.client.delete(reverse('place-detail', args=(1,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    # TODO Tests for nearby (custom action)
