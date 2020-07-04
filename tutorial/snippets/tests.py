from io import BytesIO
from django.contrib.auth.models import User
from tutorial.snippets.models import Snippet
from rest_framework.test import APITestCase, APIClient
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.urls import reverse
from pprint import pprint
from faker import Faker


class SnippetViewTest(APITestCase):

    faker = Faker()

    user = None

    snippet_count = 0

    def setUp(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = first_name[0].lower() + last_name.lower()
        email = '{}@{}'.format(username, self.faker.domain_name())
        self.user = User(first_name=first_name,
                         last_name=last_name,
                         username=username,
                         email=email)
        self.user.save()

    def new_snippet_data(self):
        title = 'Snippet ' + str(self.snippet_count + 1)
        code = 'print("Hi, World!")'
        linenos = self.faker.pybool()
        language = 'python'
        style = 'friendly'
        return title, code, linenos, language, style

    def test_snippet_list(self):
        for _ in range(10):
            (title, code, linenos, language, style) = self.new_snippet_data()
            snippet = Snippet(owner_id=self.user.id, title=title, code=code, linenos=linenos, language=language, style=style)
            snippet.save()
        client = APIClient()
        response = client.get(reverse('snippet-list'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response)
        self.assertTrue(len(response.content) > 0)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertTrue('results' in data)
        self.assertTrue(len(data['results']) == 10)
        for datum in data['results']:
            self.assertTrue('id' in datum)
            snippet = Snippet.objects.get(pk=datum['id'])
            self.assertIsNotNone(snippet)
            self.assertEqual(snippet.id, datum['id'])
            self.assertEqual(snippet.title, datum['title'])
