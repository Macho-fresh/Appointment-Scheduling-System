from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User

class RegisterTest(APITestCase):
    def test_register(self):
        data = {
            'username' : 'macho',
            'email': 'macho@gmail.com',
            'password': 'Macholina911#'
        }

        response = self.client.post(
            "/api/auth/register/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

class LoginTest(APITestCase):
    def setUp(self):

            User.objects.create_user(
                username="macho",
                email="macho@gmail.com",
                password="Password123!"
            )
    def test_login(self):
    
        data = {
            'username' : 'macho',
            'password': "Password123!"

        }  
        response = self.client.post(
            "/api/auth/login/",
            data,
            format="json"
        ) 
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        ) 

        self.assertIn('access', response.data)  
        self.assertIn('refresh', response.data)   

class RegisterProviderTest(APITestCase):
    def test_provider_register(self):
        data = {
            'username': 'macho',
            'email': 'macho@gmail.com',
            'password': "Password123!"
        }

        response = self.client.post(
            '/api/auth/register-provider/',
            data,
            format = "json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=response.data['user'])
        self.assertEqual(user.is_provider, True)
        print(response.data)