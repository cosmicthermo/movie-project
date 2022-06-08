from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app import models
from watchlist_app.api import serializers
from watchlist_app.models import StreamingService

class StreamPlatformsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="testcase")
        self.token = Token.objects.get(user__username='testcase')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamingService.objects.create(name="netflix", about="stream", website="www.netflix.com")

    def test_streamplatform_create(self):
        data = {
            'name': 'netflix',
            'about': 'about streaming stuff',
            'website': 'http://netflix.com'
        }
        response = self.client.post(reverse('streamingplatform-list'), data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamingplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_detail(self):
        response = self.client.get(reverse('streamingplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)