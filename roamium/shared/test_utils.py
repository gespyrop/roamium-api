from django.contrib.auth import get_user_model
from places.serializers import PlaceSerializer

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
    'is_wheelchair': True,
    'is_family': True,
    'is_friends': True,
}

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

def create_test_place(payload=None):
    '''Create a test place based on the given payload'''
    if payload is None:
        payload = place_payload
    serializer = PlaceSerializer(data=payload)
    serializer.is_valid()
    return serializer.save()
