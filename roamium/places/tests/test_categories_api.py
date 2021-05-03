from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from places.models import Category
from shared.test_utils import create_test_user, create_test_superuser, \
    create_test_category , category_payload
import json

CATEGORIES_URL = reverse('category-list')


class CategoryApiTest(TestCase):
    '''Tests for the Category endpoints'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = {'name': 'TestCategory'}
    
    def setUp(self):
        self.client = APIClient()
    
    def authenticateAdmin(self):
        admin = create_test_superuser()
        self.client.force_authenticate(admin)

    def authenticateRegularUser(self):
        user = create_test_user()
        self.client.force_authenticate(user)

    def test_create_category_admin_user(self):
        '''Test that admin users can create categories'''
        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.post(CATEGORIES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Check that the category was created successfuly
        category = Category.objects.get(name=self.payload['name'])
        self.assertEquals(category.name, self.payload['name'])

    def test_create_category_regular_user(self):
        '''Test that admin users can not create categories'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.post(CATEGORIES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the category was not created
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name=self.payload['name'])

    def test_create_category_unauthenticated_user(self):
        '''Test that admin users can not create categories'''
        response = self.client.post(CATEGORIES_URL, json.dumps(self.payload), content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_list_categories_authenticated_user(self):
        '''Test that authenticated users can list categories'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create 3 categories
        for _ in range(3):
            create_test_category()

        response = self.client.get(CATEGORIES_URL)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that 3 categories were returned
        self.assertEquals(len(response.data), 3)
    
    def test_list_categories_unauthenticated_user(self):
        '''Test that unauthenticated users can not list categories'''
        # Create 3 categories
        for _ in range(3):
            create_test_category()

        response = self.client.get(CATEGORIES_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)
    
    def test_retrieve_category_authenticated_user(self):
        '''Test that authenticated users can retrieve categories'''
        # Create and authenticate regular user
        self.authenticateRegularUser()

        # Create a category
        category = create_test_category()

        response = self.client.get(reverse('category-detail', args=(category.id,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the correct category was returned
        self.assertEquals(response.data['id'], category.id)

    def test_retrieve_category_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve categories'''
        # Create a category
        category = create_test_category()

        response = self.client.get(reverse('category-detail', args=(category.id,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_update_category_admin_user(self):
        '''Test that admin users can update categories'''
        # Create a category
        category = create_test_category()

        # Create and authenticate admin user
        self.authenticateAdmin()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('category-detail', args=(category.id,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the category was updated successfuly
        category = Category.objects.get(name=payload['name'])
        self.assertEquals(category.name, payload['name'])

    def test_update_category_regular_user(self):
        '''Test that admin users can not update categories'''
        # Create a category
        category = create_test_category()

        # Create and authenticate admin user
        self.authenticateRegularUser()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('category-detail', args=(category.id,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the category was not updated
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name=payload['name'])

    def test_update_category_unauthenticated_user(self):
        '''Test that admin users can not update categories'''
        # Create a test category
        category = create_test_category()

        payload = self.payload.copy()
        payload['name'] = 'New Test Name'

        response = self.client.put(reverse('category-detail', args=(category.id,)), json.dumps(payload), content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_partial_update_category_admin_user(self):
        '''Test that admin users can partially update categories'''
        # Create a test category
        category = create_test_category()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.patch(reverse('category-detail', args=(category.id,)), json.dumps({'name': 'NewName'}), content_type='application/json')

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Check that the category was updated successfuly
        category = Category.objects.get(name='NewName')
        self.assertEquals(category.name, 'NewName')

    def test_partial_update_category_regular_user(self):
        '''Test that admin users can not partially update categories'''
        # Create a category 
        category = create_test_category()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.patch(reverse('category-detail', args=(category.id,)), {'name': 'NewName'}, content_type='application/json')

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Check that the category was created successfuly
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name='NewName')

    def test_partial_update_category_unauthenticated_user(self):
        '''Test that admin users can not partially update categories'''
        # Create a test category
        category = create_test_category()

        response = self.client.patch(reverse('category-detail', args=(category.id,)), {'name': 'NewName'}, content_type='application/json')

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_category_admin_user(self):
        '''Test that admin users can destroy categories'''
        # Create a test category
        category = create_test_category()

        # Create and authenticate admin user
        self.authenticateAdmin()

        response = self.client.delete(reverse('category-detail', args=(category.id,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 204)

    def test_destroy_category_regular_user(self):
        '''Test that admin users can not destroy categories'''
        # Create a category
        category = create_test_category()

        # Create and authenticate regular user
        self.authenticateRegularUser()

        response = self.client.delete(reverse('category-detail', args=(category.id,)))

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

    def test_destroy_category_unauthenticated_user(self):
        '''Test that admin users can not destroy categories'''
        # Create a test category
        category = create_test_category()

        response = self.client.delete(reverse('category-detail', args=(category.id,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)
