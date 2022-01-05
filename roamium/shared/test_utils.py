from django.contrib.auth import get_user_model
from places.serializers import PlaceSerializer, CategorySerializer

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
    'time': '00:10:00',
    'is_bike': True,
    'wheelchair': 'no',
    'is_family': True,
    'is_friends': True,
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
