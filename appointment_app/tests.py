from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User
from .models import *

class ProviderProfileTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'macho',
            'email': 'macho@gmail.com',
            'password': "Password123!"
        }

        User.objects.create_user(
            username = 'macho',
            password = 'Password123!'
        )

        login = self.client.post(
            "/api/auth/login/",
            data,
            format="json"
        ) 
        token = login.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_provider_profile(self):
        data = {
            "specialization": "Medicine",
            "bio": "Experienced Doctor",
            "appointment_duration": "00:30:00",
            "timezone": "CAT"
        }

        response = self.client.post(
            "/api/create-provider-profile/",
            data,
            format="json"
        ) 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AvailabilityTest(APITestCase):
    def setUp(self):
        data = {
            'username': 'macho',
            'email': 'macho@gmail.com',
            'password': "Password123!"
        }

        User.objects.create_user(
            username = 'macho',
            password = 'Password123!',
            is_provider = True
        )

        login = self.client.post(
            "/api/auth/login/",
            data,
            format="json"
        ) 
        token = login.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

        ProviderProfile.objects.create(
            user = User.objects.get(id = 1),
            specialization = "Medicine",
            bio = "An experienced",
            appointment_duration = "00:30:00",
            timezone = "CAT"
        )

        Availability.objects.create(
            provider = ProviderProfile.objects.get(id = 1),
            weekday = 'Monday',
            start_time = '09:30:00',
            end_time = '17:00:00'
        )
    def test_dual_availability(self):
        data = {
            'weekday': 'Monday',
            'start_time': '09:30:00',
            'end_time': '17:00:00'
        }

        response = self.client.post(
            "/api/create-provider-availability/",
            data,
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
