from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from post.views import list_create_posts_view

User = get_user_model()

class HomePageTest(APITestCase):
    def test_homepage(self):
        response = self.client.get(reverse('post_homepage'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Hello World'})


class PostListTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = list_create_posts_view
        self.url = reverse('post_list')
        self.user = User.objects.create_user(
            username='testuser',
            email='pC0oI@example.com',
            password='testpassword'
        )

    def test_post_list(self):
        
        request = self.factory.get(self.url)

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])


    def test_post_create(self):
        sample_post = {
            'title': 'Sample title',
            'content': 'Sample content',
        }
        request = self.factory.post(self.url, sample_post)
        request.user = self.user
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
