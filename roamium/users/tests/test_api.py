from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

client = APIClient()

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
    
    def create_user(self, payload):
        return get_user_model().objects.create_user(**payload)

    def setUp(self):
        self.user = self.create_user(self.payload)
        client.force_authenticate(self.user)

    def test_create_sucessful(self):
        '''Test that user creation works'''
        endpoint = reverse('user-list')

        # Authentication not reuired for this endpoint
        client.force_authenticate(None)
    
        payload = self.payload.copy()
        payload['email'] = 'test2@email.com'
        response = client.post(endpoint, payload)

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

        # Authentication not reuired for this endpoint
        client.force_authenticate(None)

        # Create a user with the given payload
        response = client.post(endpoint, self.payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)
    
    def test_create_user_with_short_password(self):
        '''Test that the password provided is too short'''
        endpoint = reverse('user-list')

        # Authentication not reuired for this endpoint
        client.force_authenticate(None)

        payload = self.payload.copy()
        payload['email'] = 'test2@email.com'
        payload['password'] = 'abc'

        response = client.post(endpoint, payload)

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that the user was not created
        self.assertFalse(get_user_model().objects.filter(email=payload['email']).exists())
    
    def test_get_user_list(self):
        '''Test that the user list returns a list of users'''
        endpoint = reverse('user-list')

        # Create 2nd user
        payload =  self.payload.copy()
        payload['email'] = 'test2@email.com'
        self.create_user(payload)

        response = client.get(endpoint)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that 2 users were returned
        self.assertEquals(len(response.data), 2)
    
    def test_get_user(self):
        '''Test that getting the details of a specific user works'''
        endpoint = reverse('user-detail', args=[self.user.id])
        response = client.get(endpoint)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the requested user's email is included in the response
        self.assertEquals(response.data['email'], self.user.email)
    
    def test_get_user_not_exists(self):
        '''Test that getting a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[2])
        
        response = client.get(endpoint)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_update_user(self):
        '''Test that updating a user works'''
        endpoint = reverse('user-detail', args=[self.user.id])
        
        payload =  self.payload.copy()
        payload['first_name'] = 'test3'

        response = client.put(endpoint, payload)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the users first name was updated
        user = get_user_model().objects.get(**response.data)
        self.assertEquals(user.first_name, payload['first_name'])
    
    def test_update_other_user_fails(self):
        # Create other user
        payload = self.payload.copy()
        payload['email'] = 'test2@email.com'
        new_user = self.create_user(payload)

        endpoint = reverse('user-detail', args=[new_user.id])

        # Change other user's email
        payload['email'] = 'test3@email.com'
        response = client.put(endpoint, payload)

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)
    
    def test_update_user_not_exists(self):
        '''Test that updating a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[2])
        
        response = client.put(endpoint, **self.payload)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_partial_update_user(self):
        '''Test that partially updating a user works'''
        endpoint = reverse('user-detail', args=[self.user.id])
        response = client.patch(endpoint, {'first_name': 'test3'})

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the users first name was updated
        user = get_user_model().objects.get(**response.data)
        self.assertEquals(user.first_name, 'test3')
    
    def test_partial_update_other_user_fails(self):
        # Create other user
        payload =  self.payload.copy()
        payload['email'] = 'test2@email.com'
        new_user = self.create_user(payload)

        endpoint = reverse('user-detail', args=[new_user.id])
        response = client.patch(endpoint, {'first_name': 'test3'})

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)
    
    def test_partial_update_user_not_exists(self):
        '''Test that partially updating a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[2])
        
        response = client.put(endpoint, {'first_name': 'test3'})

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
    
    def test_delete_user_exists(self):
        '''Test that user deletion works'''
        endpoint = reverse('user-detail', args=[self.user.id])
        
        response = client.delete(endpoint)

        # Test that the response status code is 204
        self.assertEquals(response.status_code, 204)

        # Test that the user was deleted
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())
    
    def test_delete_other_user_fails(self):
        # Create other user
        payload =  self.payload.copy()
        payload['email'] = 'test2@email.com'
        new_user = self.create_user(payload)

        endpoint = reverse('user-detail', args=[new_user.id])
        response = client.delete(endpoint)

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)
    
    def test_delete_user_not_exists(self):
        '''Test that deleting a user with an invalid ID returns a 404'''
        endpoint = reverse('user-detail', args=[2])
        
        response = client.delete(endpoint)

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)


class TokenTests(TestCase):
    '''Tests for the JWT endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = {
            'email': 'test@email.com',
            'password': 'testpass',
            'first_name': 'testF',
            'last_name': 'testL',
        }
    
    def test_obtain_token(self):
        '''Test that the token_obtain_pair endpoint returns a token for valid user credentials'''
        endpoint = reverse('token_obtain_pair')
        get_user_model().objects.create_user(**self.payload)
        response = client.post(endpoint, self.payload)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that an access token and a refresh token is returned in the payload
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_token_invalid_user(self):
        '''Test that the token_obtain endpoint responds with an error message for invalid user credentials'''
        endpoint = reverse('token_obtain_pair')
        response = client.post(endpoint, self.payload)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that an access token is not returned in the payload
        self.assertNotIn('access', response.data)

        # Test that an error message is returned
        self.assertIn('detail', response.data)
    
    def test_refresh_token(self):
        '''Test that the refresh_token endpoint returns a new access token when a valid refresh token is provided'''
        get_user_model().objects.create_user(**self.payload)
        refresh_token = client.post(reverse('token_obtain_pair'), self.payload).data['refresh']

        endpoint = reverse('token_refresh')
        response = client.post(endpoint, {'refresh': refresh_token})

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that a new access token is returned
        self.assertIn('access', response.data)

    def test_refresh_token_invalid_user(self):
        '''Test that the refresh_token endpoint does not return a new access token when an invalid refresh token is provided'''
        endpoint = reverse('token_refresh')
        response = client.post(endpoint, {'refresh': 'asdfasfasdf'})

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that an access token is not returned in the payload
        self.assertNotIn('access', response.data)

        # Test that an error message is returned
        self.assertIn('detail', response.data)
