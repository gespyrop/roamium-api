from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class UserTests(TestCase):
    '''Tests for the User endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = 'user:{}'
        self.payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'first_name': 'testF',
            'last_name': 'testL',
        }

    def setUp(self):
        self.client = APIClient()

    def test_create_sucessful(self):
        '''Test that user creation works'''
        endpoint = self.endpoint.format('create')
        payload = self.payload.copy()
        response = self.client.post(endpoint, payload)

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Check that the user's password was set correctly 
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))

        # Check that the password is not returned in the response
        self.assertNotIn('password', response.data)

    def test_create_user_with_existing_email(self):
        '''Test that user creation fails if there is already a user with the given email'''
        endpoint = self.endpoint.format('create')
        payload = self.payload.copy()

        # Create a user with the given payload
        get_user_model().objects.create(**payload)
        response = self.client.post(endpoint, payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)
    
    def test_create_user_with_short_password(self):
        '''Test that the password provided is too short'''
        endpoint = self.endpoint.format('create')
        payload = self.payload.copy()
        payload['password'] = 'abc'

        response = self.client.post(endpoint, payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that the user was not created
        self.assertIsNone(get_user_model().objects.get(email=payload['email']))
