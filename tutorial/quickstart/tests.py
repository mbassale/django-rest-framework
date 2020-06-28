from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from pprint import pprint
from faker import Faker


class UserViewSetTest(APITestCase):

    faker = Faker()

    def new_user_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = first_name[0].lower() + last_name.lower()
        email = '{}@{}'.format(username, self.faker.domain_name())
        return first_name, last_name, username, email

    def test_get(self):
        (first_name, last_name, username, email) = self.new_user_data()
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
        new_user.save()
        client = APIClient()
        response = client.get(reverse('user-list'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEquals(response.data['count'], 1)
        self.assertIsNotNone(response.data['results'])
        for user_data in response.data['results']:
            self.assertTrue('id' in user_data)
            self.assertTrue(user_data['id'], new_user.id)

    def test_post(self):
        self.assertEquals(User.objects.count(), 0)
        client = APIClient()
        (first_name, last_name, username, email) = self.new_user_data()
        response = client.post(reverse('user-list'), {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        })
        self.assertIsNotNone(response)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.data['id'] > 0)
        self.assertEquals(User.objects.count(), 1)
        user = User.objects.get(pk=response.data['id'])
        self.assertIsNotNone(user)
        self.assertEquals(user.username, username)
        self.assertEquals(user.first_name, first_name)
        self.assertEquals(user.last_name, last_name)
        self.assertEquals(user.email, email)


