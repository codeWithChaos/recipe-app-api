"""Tests for the user api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token') # URL endpoint for creating tokens

# Helper function to create a user
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user api"""
    
    def setUp(self):
        self.client = APIClient() # Create an API client for testing

    def test_create_user_success(self):
        """Test creating a user is successful."""
        # Payload for testing the api
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload) # making a post request to the created url

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password'])) # 
        self.assertNotIn('passsword', res.data)  # Make sure the password is not return in the response for security reasons

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload) # takes payload and call the create user to create a new user
        res = self.client.post(CREATE_USER_URL, payload) # make a post request to the url

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # check for bad request

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists() # check that it doesn't create a user
        self.assertFalse(user_exists) # Confirm user doesn't actually exist in the database
        
    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_datails = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password'
        }
        create_user(**user_datails)

        payload = {
        'email': user_datails['email'],
        'password': user_datails['password'],
        }
        res = self.client.post(TOKEN_URL, payload) # POST the payload to the token url

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTO_400_BAD_REQUEST)

    def create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': 'tes@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)