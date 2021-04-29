from django.contrib.auth import get_user_model

user_payload = {
    'email': 'test@email.com',
    'password': 'testpass',
    'first_name': 'testF',
    'last_name': 'testL',
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