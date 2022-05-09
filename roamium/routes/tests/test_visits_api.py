from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from routes.models import Visit
from shared.test_utils import create_test_route, create_test_user,\
    create_test_place, create_test_visit,\
    create_visit_payload, user_payload
import json

VISITS_URL = reverse('visit-list')


class VisitApiTest(TestCase):
    '''Tests for the Visit endpoints'''

    def setUp(self):
        self.user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_visit(self):
        '''Test that users can create visits'''
        route = create_test_route(self.user)
        place = create_test_place()
        payload = create_visit_payload(place, route)

        response = self.client.post(
            VISITS_URL, json.dumps(payload), content_type='application/json'
        )

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Test that the visit was created successfully
        self.assertEquals(route.visit_set.count(), 1)
        self.assertEquals(route.visit_set.first().name, place.name)

    def test_create_visit_unauthenticated_user(self):
        '''Test that unauthanticated users can not create visits'''
        # Log the user out
        self.client.logout()

        route = create_test_route(self.user)
        place = create_test_place()
        payload = create_visit_payload(place, route)

        response = self.client.post(
            VISITS_URL, json.dumps(payload), content_type='application/json'
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that a route was not created
        self.assertEquals(Visit.objects.count(), 0)

    def test_create_visit_different_user(self):
        '''Test that users can not create visits from other users' routes'''
        route = create_test_route(self.user)

        different_user = create_test_user(
            user_payload.update(email='test6@email.com')
        )

        # Login as differenct user
        self.client.force_authenticate(different_user)

        place = create_test_place()
        payload = create_visit_payload(place, route)

        response = self.client.post(
            VISITS_URL, json.dumps(payload), content_type='application/json'
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Test that a route was not created
        self.assertEquals(Visit.objects.count(), 0)

    def test_list_visits(self):
        '''Test that users can list their visits only'''
        # Create visit for authenticated user
        route = create_test_route(self.user)
        place = create_test_place()
        create_test_visit(place, route)

        # Create visit for different user
        different_user = create_test_user(
            user_payload.update(email='test7@email.com')
        )
        different_route = create_test_route(different_user)
        create_test_visit(place, different_route)

        response = self.client.get(VISITS_URL)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the user listed only their visits
        self.assertEquals(len(response.data), 1)

    def test_list_visits_unauthenticated_user(self):
        '''Test that unauthenticated users can not list visits'''
        # Log the user out
        self.client.logout()

        response = self.client.get(VISITS_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_retrieve_visit(self):
        '''Test that users can retrieve their visits'''
        route = create_test_route(self.user)
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.get(reverse('visit-detail', args=(visit.id,)))

        # Test that the response status code is 200
        self.assertAlmostEquals(response.status_code, 200)

        # Test that the visit was returned
        self.assertEquals(response.data['id'], visit.id)

    def test_retrieve_visit_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve visits'''
        # Log the user out
        self.client.logout()

        # Create a visit
        route = create_test_route(self.user)
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.get(reverse('visit-detail', args=(visit.id,)))

        # Test that the response status code is 401
        self.assertAlmostEquals(response.status_code, 401)

    def test_retrieve_visit_different_user(self):
        '''Test that users can not retrieve visits from other users'''
        # Create visit for different user
        different_user = create_test_user(
            user_payload.update(email='test8@email.com')
        )
        different_route = create_test_route(different_user)
        place = create_test_place()
        visit = create_test_visit(place, different_route)

        response = self.client.get(reverse('visit-detail', args=(visit.id,)))

        # Test that the response status code is 404
        self.assertAlmostEquals(response.status_code, 404)

    def test_destroy_visit(self):
        '''Test that users can destroy their visits'''
        # Create a visit
        route = create_test_route(self.user)
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.delete(
            reverse('visit-detail', args=(visit.id,))
        )

        # Test that the response status code is 204
        self.assertEquals(response.status_code, 204)

        # Test that the visit was deleted
        self.assertEquals(Visit.objects.count(), 0)

    def test_destroy_visit_unauthenticated_users(self):
        '''Test that unauthenticated users can not destroy visits'''
        # Log the user out
        self.client.logout()

        # Create a visit
        route = create_test_route(self.user)
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.delete(
            reverse('visit-detail', args=(visit.id,))
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_visit_different_user(self):
        '''Test that users can not destroy other users' visits'''
        # Create a visit for a different user
        different_user = create_test_user(
            user_payload.update(email='test9@email.com')
        )
        route = create_test_route(different_user)
        place = create_test_place()
        visit = create_test_visit(place, route)

        response = self.client.delete(
            reverse('visit-detail', args=(visit.id,))
        )

        # Test that the response status code is 404
        self.assertEquals(response.status_code, 404)
