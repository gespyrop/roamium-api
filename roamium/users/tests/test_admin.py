from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin = get_user_model().objects.create_superuser(
            email='admin@email.com',
            first_name='AdminF',
            last_name='AdminL',
            password='adminpassword'
        )
        # Log the admin user in
        self.client.force_login(self.admin)

        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            first_name='TestF',
            last_name='TestL',
            password='testpassword'
        )
    
    def test_user_changelist(self):
        '''Test that the users are listed in the user page of the admin webpage.'''
        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)

    def test_user_change(self):
        '''Test that the user edit page works.'''
        url = reverse('admin:users_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)

    def test_user_add(self):
        '''Test that the user add page works.'''
        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
