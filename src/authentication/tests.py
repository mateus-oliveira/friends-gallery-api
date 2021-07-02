from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
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
