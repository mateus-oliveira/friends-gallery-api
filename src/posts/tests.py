from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker

from .models import Post


class PostTests(APITestCase):
    def test_create_post(self):
        url = reverse('posts_urls:posts-list')
        user = baker.make('authentication.User', role=1)
        asset = baker.make('asset.Asset')

        self.client.force_authenticate(user)

        body = {
            'asset': asset.id,
            'user': user.id,
            'caption': 'Happy merried',
            'likes': [user.id],
        }

        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.get().caption, 'Happy merried')
        self.assertEqual(Post.objects.get().asset, asset)

    def test_dont_create_post_if_is_offline(self):
        url = reverse('posts_urls:posts-list')
        user = baker.make('authentication.User', role=1)
        asset = baker.make('asset.Asset')

        body = {
            'asset': asset.id,
            'user': user.id,
            'caption': 'Happy merried',
            'likes': [user.id],
        }

        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
