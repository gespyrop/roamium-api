from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with email'''
        email = 'test@email.com'
        password = 'testpassword'
        first_name = 'testfirstname'
        last_name = 'testlastname'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        '''Test creating user with no email creates error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testfirstname', 'testlastname', 'testpassword')
    
    def test_new_user_invalid_fisrt_name(self):
        '''Test creating user with no fisrt name creates error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@email.com', None, 'testlastname', 'testpassword')
    
    def test_new_user_invalid_last_name(self):
        '''Test creating user with no last name creates error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@email.com', 'testfirstname', None, 'testpassword')
    
    def test_create_new_superuser(self):
        '''Test creating a new admin with email'''
        email = 'test@email.com'
        password = 'testpassword'
        first_name = 'testfirstname'
        last_name = 'testlastname'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
