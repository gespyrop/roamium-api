from django.contrib.auth import get_user_model

from places.serializers import PlaceSerializer, CategorySerializer
from routes.serializers import ReviewSerializer, VisitSerializer
from routes.models import Route


user_payload = {
    'email': 'test@email.com',
    'password': 'testpass',
    'first_name': 'testF',
    'last_name': 'testL',
}

place_payload = {
    'name': 'TestPlace',
    'location': {
        'latitude': 0.0,
        'longitude': 0.0
    },
    'wheelchair': 'no',
}

category_payload = {'name': 'TestPlace'}


def create_test_user(payload=None):
    '''Create a test user based on the given payload'''
    if payload is None:
        payload = user_payload
    return get_user_model().objects.create_user(**payload)


def create_test_superuser(payload=None):
    '''Create a test superuser based on the given payload'''
    if payload is None:
        payload = user_payload
    return get_user_model().objects.create_superuser(**payload)


def create_test_place(**kwargs):
    '''Create a test place based on the given payload'''
    payload = dict(place_payload, **kwargs)
    serializer = PlaceSerializer(data=payload)
    serializer.is_valid()
    return serializer.save()


def create_test_category(**kwargs):
    '''Create a test category based on the given payload'''
    payload = dict(category_payload, **kwargs)
    serializer = CategorySerializer(data=payload)
    serializer.is_valid()
    return serializer.save()


def create_visit_payload(place, route):
    return {
        'place_id': place.id,
        'place_source': 'roamium',
        'name': place.name,
        'route': route.id
    }


def create_review_payload(visit):
    return {
        'visit': visit.id,
        'stars': 3,
        'text': 'Review text'
    }


def create_test_route(user):
    return Route.objects.create(user=user)


def create_test_visit(place, route):
    '''Create a test visit for the given place and route'''
    payload = create_visit_payload(place, route)
    serializer = VisitSerializer(data=payload)
    serializer.is_valid()
    return serializer.save()


def create_test_review(visit):
    '''Create a test review for the given visit'''
    payload = create_review_payload(visit)
    serializer = ReviewSerializer(data=payload)
    serializer.is_valid()
    return serializer.save()
