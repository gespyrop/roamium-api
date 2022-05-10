from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from routes.models import Route
from shared.test_utils import create_test_place, create_test_route,\
    create_test_user, create_test_visit, user_payload

ROUTES_URL = reverse('route-list')


class RouteApiTest(TestCase):
    '''Tests for the Route endpoints'''

    def setUp(self):
        self.user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_route(self):
        '''Test that users can create routes'''
        response = self.client.post(ROUTES_URL)

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Test that the route was created successfully
        self.assertEquals(Route.objects.filter(user=self.user).count(), 1)

    def test_create_route_unauthenticated_user(self):
        '''Test that unauthanticated users can not create routes'''
        # Log the user out
        self.client.logout()

        response = self.client.post(ROUTES_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that a route was not created
        self.assertEquals(Route.objects.count(), 0)

    def test_list_routes(self):
        '''Test that users can list their routes only'''
        # Create a route
        route = create_test_route(self.user)

        # Create a visit
        place = create_test_place()
        visit = create_test_visit(place, route)

        # Create route for different user
        different_user = create_test_user(
            user_payload.update(email='test2@email.com')
        )

        create_test_route(different_user)

        response = self.client.get(ROUTES_URL)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the user listed only their routes
        self.assertEquals(len(response.data), 1)

        # Test that the visits were returned in the response body
        visits = response.data[0]['visits']
        self.assertEquals(len(visits), 1)
        self.assertEquals(visits[0]['id'], visit.id)

    def test_list_routes_unauthenticated_user(self):
        '''Test that unauthenticated users can not list routes'''
        # Log the user out
        self.client.logout()

        response = self.client.get(ROUTES_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_retrieve_route(self):
        '''Test that users can retrieve their routes'''
        # Create a route
        route = create_test_route(self.user)

        # Create a visit
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.get(reverse('route-detail', args=(route.id,)))

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the route was returned
        self.assertEquals(response.data['id'], route.id)

        # Test that the visits were returned in the response body
        visits = response.data['visits']
        self.assertEquals(len(visits), 1)
        self.assertEquals(visits[0]['id'], visit.id)

    def test_retrieve_route_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve routes'''
        # Log the user out
        self.client.logout()

        # Create a route
        route = create_test_route(self.user)

        response = self.client.get(reverse('route-detail', args=(route.id,)))

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_retrieve_route_different_user(self):
        '''Test that users can not retrieve routes from other users'''
        # Create route for different user
        different_user = create_test_user(
            user_payload.update(email='test3@email.com')
        )

        route = create_test_route(different_user)

        response = self.client.get(reverse('route-detail', args=(route.id,)))

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)

    def test_destroy_route(self):
        '''Test that users can destroy their routes'''
        # Create a route
        route = create_test_route(self.user)

        response = self.client.delete(
            reverse('route-detail', args=(route.id,))
        )

        # Test that the response status code is 204
        self.assertEquals(response.status_code, 204)

        # Test that the route was deleted
        self.assertEquals(Route.objects.count(), 0)

    def test_destroy_route_unauthenticated_users(self):
        '''Test that unauthenticated users can not destroy routes'''
        # Log the user out
        self.client.logout()

        # Create a route
        route = create_test_route(self.user)

        response = self.client.delete(
            reverse('route-detail', args=(route.id,))
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_route_different_user(self):
        '''Test that users can not destroy other users' routes'''
        # Create a route for a different user
        different_user = create_test_user(
            user_payload.update(email='test4@email.com')
        )

        route = create_test_route(different_user)

        response = self.client.delete(
            reverse('route-detail', args=(route.id,))
        )

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)

    def test_complete_route(self):
        '''Test that users can complete a route of theirs'''
        # Create a route
        route = create_test_route(self.user)

        response = self.client.post(
            reverse('route-complete', args=(route.id,))
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the route was marked as finished
        self.assertTrue(response.data['finished'])
        self.assertTrue(Route.objects.get(pk=route.id).finished)

    def test_complete_route_unauthenticated_user(self):
        '''Test that unauthenticated users can not complete routes'''
        # Log the user out
        self.client.logout()

        # Create a route
        route = create_test_route(self.user)

        response = self.client.post(
            reverse('route-complete', args=(route.id,))
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that the route was not marked as finished
        self.assertFalse(Route.objects.get(pk=route.id).finished)

    def test_complete_route_different_user(self):
        '''Test that users can not complete other user's routes'''
        # Create a route for a different user
        different_user = create_test_user(
            user_payload.update(email='test5@email.com')
        )

        route = create_test_route(different_user)

        response = self.client.post(
            reverse('route-complete', args=(route.id,))
        )

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
