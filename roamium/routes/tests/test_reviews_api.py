import json
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from routes.models import Review
from shared.test_utils import create_review_payload, create_test_place,\
    create_test_review, create_test_route, create_test_user,\
    create_test_visit, user_payload


REVIEWS_URL = reverse('review-list')

CONTENT_TYPE = 'application/json'
UPDATED_REVIEW_TEXT = 'New review text'


class ReviewApiTest(TestCase):
    '''Tests for the Review endpoints'''

    def setUp(self):
        self.user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.visit = self.create_visit(self.user)

    def create_visit(self, user):
        # Create a route
        route = create_test_route(user)

        # Create a visit
        place = create_test_place()
        visit = create_test_visit(place, route)

        return visit

    def test_create_review(self):
        '''Test that users can create reviews'''
        # Review payload
        payload = create_review_payload(self.visit)

        response = self.client.post(
            REVIEWS_URL, json.dumps(payload), content_type=CONTENT_TYPE
        )

        # Test that the response status code is 201
        self.assertEquals(response.status_code, 201)

        # Test that the review was created successfully
        self.assertEquals(Review.objects.count(), 1)
        self.assertEquals(response.data['id'], self.visit.review.id)

    def test_create_review_unauthenticated_user(self):
        '''Test that unauthenticated users can not create reviews'''
        # Log the user out
        self.client.logout()

        # Review payload
        payload = create_review_payload(self.visit)

        response = self.client.post(
            REVIEWS_URL, json.dumps(payload), content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

        # Test that the review was not created
        self.assertEquals(Review.objects.count(), 0)

    def test_create_review_different_user(self):
        '''Test that users can not create reviews for other users' visits'''
        different_user = create_test_user(
            user_payload.update(email='test10@email.com')
        )

        self.client.force_authenticate(different_user)

        # Review payload
        payload = create_review_payload(self.visit)

        response = self.client.post(
            REVIEWS_URL, json.dumps(payload), content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

        # Test that a review was not created
        self.assertEquals(Review.objects.count(), 0)

    def test_list_routes(self):
        '''Test that users can list their reviews'''
        # Create a review
        create_test_review(self.visit)

        # Create review for different user
        different_user = create_test_user(
            user_payload.update(email='test11@email.com')
        )
        self.create_visit(different_user)

        response = self.client.get(REVIEWS_URL)

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the user listed only their reviews
        self.assertEquals(len(response.data), 1)

    def test_list_visits_unauthenticated_user(self):
        '''Test that unauthenticated users can not list reviews'''
        # Log the user out
        self.client.logout()

        response = self.client.get(REVIEWS_URL)

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_retrieve_review(self):
        '''Test that users can retrieve reviews'''
        review = create_test_review(self.visit)

        response = self.client.get(
            reverse('review-detail', args=(review.id,))
        )

        # Test that the response status code is 200
        self.assertAlmostEquals(response.status_code, 200)

        # Test that the reviews was returned
        self.assertEquals(response.data['id'], review.id)

    def test_retrieve_review_unauthenticated_user(self):
        '''Test that unauthenticated users can not retrieve reviews'''
        # Log the user out
        self.client.logout()

        # Create a review
        review = create_test_review(self.visit)

        response = self.client.get(reverse('review-detail', args=(review.id,)))

        # Test that the response status code is 401
        self.assertAlmostEquals(response.status_code, 401)

    def test_update_review(self):
        '''Test that users can update their views'''
        # Create a review
        review = create_test_review(self.visit)

        # New review payload
        payload = {
            'visit': self.visit.id,
            'text': UPDATED_REVIEW_TEXT,
            'stars': 4
        }

        response = self.client.put(
            reverse('review-detail', args=(review.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the review was updated
        updated_review = Review.objects.get(pk=review.id)
        self.assertEquals(updated_review.stars, 4)
        self.assertEquals(updated_review.text, UPDATED_REVIEW_TEXT)

    def test_update_review_unauthenticated_user(self):
        '''Test that unauthenticated users can not update reviews'''
        # Log the user out
        self.client.logout()

        # Create a review
        review = create_test_review(self.visit)

        # New review payload
        payload = {
            'visit': self.visit.id,
            'text': UPDATED_REVIEW_TEXT,
            'stars': 4
        }

        response = self.client.put(
            reverse('review-detail', args=(review.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_update_review_different_user(self):
        '''Test that users can not update other users' reviews'''
        # Create a review for a different user
        different_user = create_test_user(
            user_payload.update(email='test12@email.com')
        )
        different_visit = self.create_visit(different_user)

        review = create_test_review(different_visit)

        # New review payload
        payload = {
            'visit': self.visit.id,
            'text': UPDATED_REVIEW_TEXT,
            'stars': 4
        }

        response = self.client.put(
            reverse('review-detail', args=(review.id,)),
            json.dumps(payload),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

    def test_partial_update_review(self):
        '''Test that users can update their views partially'''
        # Create a review
        review = create_test_review(self.visit)

        response = self.client.patch(
            reverse('review-detail', args=(review.id,)),
            json.dumps({'stars': 4}),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the review was updated
        updated_review = Review.objects.get(pk=review.id)
        self.assertEquals(updated_review.stars, 4)

    def test_partial_update_review_unauthenticated_user(self):
        '''Test that unauthenticated users can not update reviews partially'''
        # Log the user out
        self.client.logout()

        # Create a review
        review = create_test_review(self.visit)

        response = self.client.patch(
            reverse('review-detail', args=(review.id,)),
            json.dumps({'stars': 4}),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_partial_update_review_different_user(self):
        '''Test that users can not update other users' reviews partially'''
        # Create a review for a different user
        different_user = create_test_user(
            user_payload.update(email='test13@email.com')
        )
        different_visit = self.create_visit(different_user)

        review = create_test_review(different_visit)

        response = self.client.patch(
            reverse('review-detail', args=(review.id,)),
            json.dumps({'stars': 4}),
            content_type=CONTENT_TYPE
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

    def test_destroy_review(self):
        '''Test that users can destroy their reviews'''
        # Create a review
        review = create_test_review(self.visit)

        response = self.client.delete(
            reverse('review-detail', args=(review.id,))
        )

        # Test that the response status code is 204
        self.assertEquals(response.status_code, 204)

        # Test that the review was deleted
        self.assertEquals(Review.objects.count(), 0)

    def test_destroy_review_unauthenticated_users(self):
        '''Test that unauthenticated users can not destroy review'''
        # Log the user out
        self.client.logout()

        # Create a review
        review = create_test_review(self.visit)

        response = self.client.delete(
            reverse('review-detail', args=(review.id,))
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_destroy_review_different_user(self):
        '''Test that users can not destroy other users' reviews'''
        # Create a review for a different user
        different_user = create_test_user(
            user_payload.update(email='test14@email.com')
        )
        different_visit = self.create_visit(different_user)

        review = create_test_review(different_visit)

        response = self.client.delete(
            reverse('review-detail', args=(review.id,))
        )

        # Test that the response status code is 403
        self.assertEquals(response.status_code, 403)

    def test_get_place_reviews(self):
        '''Test that users can get reviews for a place'''
        review = create_test_review(self.visit)

        place_id = self.visit.place_id

        response = self.client.get(
            f'{REVIEWS_URL}place/?source=roamium&place_id={place_id}'
        )

        # Test that the response status code is 200
        self.assertEquals(response.status_code, 200)

        # Test that the review was returned
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['id'], review.id)

    def test_get_place_reviews_no_source(self):
        '''Test that the source parameter is required for place reviews.'''
        response = self.client.get(
            f'{REVIEWS_URL}place/'
        )

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

    def test_get_place_reviews_invalid_source(self):
        '''
        Test that invalid source parameters are not accepted for place reviews.
        '''
        response = self.client.get(
            f'{REVIEWS_URL}place/?source=test'
        )

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that an error message was returned
        self.assertEquals(
            response.data['message'], "'test' is not in (roamium,osm)."
        )

    def test_get_place_reviews_no_place_id(self):
        '''Test that the place_id parameter is required for place reviews.'''
        response = self.client.get(
            f'{REVIEWS_URL}place/?source=roamium'
        )

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that an error message was returned
        self.assertEquals(
            response.data['message'], "Parameter 'place_id' is required."
        )

    def test_get_place_reviews_invalid_place_id(self):
        '''Test that the place_id parameter must be an integer.'''
        response = self.client.get(
            f'{REVIEWS_URL}place/?source=roamium&place_id=test'
        )

        # Test that the response status code is 400
        self.assertEquals(response.status_code, 400)

        # Test that an error message was returned
        self.assertEquals(
            response.data['message'],
            "Parameter 'place_id' must be an integer."
        )

    def test_get_place_reviews_unauthenticated_user(self):
        '''Test that unauthenticated users can not get reviews for a place'''
        # Log the user out
        self.client.logout()

        create_test_review(self.visit)
        place_id = self.visit.place_id

        response = self.client.get(
            f'{REVIEWS_URL}place/?source=roamium&place_id={place_id}'
        )

        # Test that the response status code is 401
        self.assertEquals(response.status_code, 401)

    def test_places_average_rating(self):
        '''Test that the average rating is returned in the places payload.'''
        # Create a route
        route = create_test_route(self.user)

        # Create two visits
        place = create_test_place()

        visit = create_test_visit(place, route)
        create_test_review(visit)

        visit = create_test_visit(place, route)
        review = create_test_review(visit)

        # Change second review's stars to 4
        review.stars = 4
        review.save()

        response = self.client.get(
            reverse('place-detail', args=(visit.place_id,))
        )

        # Test that the average rating of the place was included
        self.assertEquals(response.data['rating'], 3.5)
