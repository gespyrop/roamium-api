from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class UserTests(TestCase):
    '''Tests for the User endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        endpoint = reverse('user-list')
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
        endpoint = reverse('user-list')
        payload = self.payload.copy()

        # Create a user with the given payload
        get_user_model().objects.create(**payload)
        response = self.client.post(endpoint, payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)
    
    def test_create_user_with_short_password(self):
        '''Test that the password provided is too short'''
        endpoint = reverse('user-list')
        payload = self.payload.copy()
        payload['password'] = 'abc'

        response = self.client.post(endpoint, payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that the user was not created
        self.assertFalse(get_user_model().objects.filter(email=payload['email']).exists())
    
    def test_get_user_list(self):
        '''Test that the user list returns a list of users'''
        endpoint = reverse('user-list')
        payload =  self.payload.copy()

        # Crete 2 users
        get_user_model().objects.create(**payload)
        payload['email'] = 'test2@email.com'
        get_user_model().objects.create(**payload)

        response = self.client.get(endpoint)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that 2 users were returned
        self.assertEquals(len(response.data), 2)
    
    def test_get_user(self):
        '''Test that getting the details of a specific user works'''
        payload =  self.payload.copy()
        user = get_user_model().objects.create(**payload)

        endpoint = reverse('user-detail', args=[user.id])
        response = self.client.get(endpoint)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the requested user's email is included in the response
        self.assertEquals(response.data['email'], user.email)
    
    def test_get_user_not_exists(self):
        '''Test that getting a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[1])
        
        response = self.client.get(endpoint)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_update_user(self):
        '''Test that updating a user works'''
        payload =  self.payload.copy()
        user = get_user_model().objects.create(**payload)

        payload['first_name'] = 'test3'
        endpoint = reverse('user-detail', args=[user.id])
        response = self.client.put(endpoint, payload)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the users first name was updated
        user = get_user_model().objects.get(**response.data)
        self.assertEquals(user.first_name, payload['first_name'])
    
    def test_update_user_not_exists(self):
        '''Test that updating a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[1])
        
        response = self.client.put(endpoint, **self.payload)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_partial_update_user(self):
        '''Test that partially updating a user works'''
        user = get_user_model().objects.create(**self.payload)

        endpoint = reverse('user-detail', args=[user.id])
        response = self.client.patch(endpoint, {'first_name': 'test3'})

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the users first name was updated
        user = get_user_model().objects.get(**response.data)
        self.assertEquals(user.first_name, 'test3')
    
    def test_partial_update_user_not_exists(self):
        '''Test that partially updating a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[1])
        
        response = self.client.put(endpoint, {'first_name': 'test3'})

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_delete_user_exists(self):
        '''Test that user deletion works'''
        user = get_user_model().objects.create(**self.payload)
        endpoint = reverse('user-detail', args=[user.id])
        
        response = self.client.delete(endpoint)

        # Test that the response status code is 204
        self.assertEquals(response.status_code, 204)

        # Test that the user was deleted
        self.assertFalse(get_user_model().objects.filter(id=user.id).exists())
    
    def test_delete_user_not_exists(self):
        '''Test that deleting a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[1])
        
        response = self.client.delete(endpoint)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
