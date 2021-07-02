from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_bakery import baker

from .models import Comment, Post


class PostTests(APITestCase):
    def test_create_post(self):
        url = reverse('post_urls:posts-list')
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

    def test_dont_create_post_offline(self):
        url = reverse('post_urls:posts-list')
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

    def test_like_a_post(self):
        post = baker.make('post.Post', status=2)
        url = reverse("post_urls:posts-like", args=[post.id])

        user = baker.make('authentication.User')
        self.client.force_authenticate(user)

        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().likes.all()[0], user)

    def test_unlike_a_post(self):
        user = baker.make('authentication.User')
        post = baker.make('post.Post', status=2, likes=[user])
        url = reverse("post_urls:posts-like", args=[post.id])
        self.client.force_authenticate(user)

        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Post.objects.get().likes.all()), 0)


class CommentTest(APITestCase):
    def test_comment_a_post(self):
        post = baker.make('post.Post', status=2)
        url = reverse("post_urls:comments-list")

        user = baker.make('authentication.User')
        self.client.force_authenticate(user)

        body = {
            'post': post.id,
            'user': user.id,
            'text': 'I liked!',
        }

        response = self.client.post(url, body, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.get().text, 'I liked!')
        self.assertEqual(Comment.objects.get().post, post)
        self.assertEqual(Comment.objects.get().user, user)

    def test_dont_comment_a_post_offline(self):
        post = baker.make('post.Post', status=2)
        url = reverse("post_urls:comments-list")

        user = baker.make('authentication.User')

        body = {
            'post': post.id,
            'user': user.id,
            'text': 'I liked!',
        }

        response = self.client.post(url, body, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
