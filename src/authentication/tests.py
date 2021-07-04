from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django_rest_passwordreset.models import ResetPasswordToken
from model_bakery import baker

from .models import User


class AuthenticationTests(APITestCase):
    def test_create_user(self):
        url = reverse('authentication_urls:users-list')
        body = {
            "first_name": "Marido",
            "last_name": "Husband",
            "email": "husband@gallery.com",
            "username": "husband",
            "password": "ilovemywife",
            "role": 1,
        }
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().email, 'husband@gallery.com')
        self.assertEqual(User.objects.get().first_name, "Marido")

    def test_login_success(self):
        url = reverse('login')
        baker.make(User, email="husband@gallery.com", password='ilovemywife')

        body = {
            "email": "husband@gallery.com",
            "password": 'ilovemywife',
        }
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        url = reverse('login')
        baker.make(User, email="husband@gallery.com", password='ilovemywife')

        body = {
            "email": "husband@gallery.com",
            "password": "ihatemywife",
        }
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recover_password(self):
        old_password = 'gallery'
        new_password = 'gallery2021'
        email = 'friend@friend.app'

        url = reverse('reset-password:reset-password-request')
        baker.make(
            'authentication.User',
            email=email,
            password=old_password,
        )

        body = {
            "email": email,
        }

        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = ResetPasswordToken.objects.get().key

        url = reverse('reset-password:reset-password-confirm')
        body = {
            "token": token,
            "password": new_password,
        }

        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('login')
        body = {
            "email": email,
            "password": new_password,
        }
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
