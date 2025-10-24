'''test for user api'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL=reverse('user:create')


def create_user(**params):
    '''create and return new user'''
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    '''test the public features of the user api'''
    def setUp(self):
        self.client=APIClient()


    def test_create_user_success(self):
        '''test creating a user is successful'''
        payload={
            'email':'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res=self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_existing_email_error(self):
        '''test error returned if user with email exists'''
        payload={
            'email':'test@eaxmple.com',
            'password':'test123pass',
            'name':'Test Name',
        }
        create_user(**payload)

        res=self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        '''test an error is retuned if password is less than 5 chars'''
        payload={
            'email': 'test@example.com',
            'password':'pw',
            'name':'Test name',
        }

        res=self.client.post(CREATE_USER_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists=get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

from rest_framework.authtoken.models import Token

TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test token is created for valid credentials"""
        user_details = {
            'email': 'test@example.com',
            'password': 'pass1234',
            'name': 'Test'
        }
        create_user(**user_details)

        payload = {'email': user_details['email'], 'password': user_details['password']}
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token not created with invalid credentials"""
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='user@example.com',
            password='testpass',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged-in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'email': self.user.email, 'name': self.user.name})

    def test_post_me_not_allowed(self):
        """Test POST is not allowed on the me endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile"""
        payload = {'name': 'New name', 'password': 'newpass123'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)





