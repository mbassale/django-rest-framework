from io import BytesIO
from tutorial.snippets.models import Snippet
from tutorial.snippets.serializers import SnippetSerializer
from rest_framework.test import APITestCase, APIClient
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.urls import reverse
from pprint import pprint
from faker import Faker


class SnippetSerializerTest(APITestCase):
    faker = Faker()

    def test_serialize(self):
        # test serialization
        snippet = Snippet(code='print("Hello, world")\n')
        snippet.save()
        self.assertEquals(Snippet.objects.count(), 1)
        serializer = SnippetSerializer(snippet)
        content = serializer.data
        self.assertIsNotNone(content)
        self.assertTrue('id' in content and
                        'title' in content and
                        'code' in content and
                        'language' in content)

        # convert to json
        content = JSONRenderer().render(serializer.data)
        self.assertIsNotNone(content)

        # test deserialization and creation
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = SnippetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue('title' in serializer.validated_data and
                        'code' in serializer.validated_data and
                        'language' in serializer.validated_data)
        new_snippet = serializer.save()
        self.assertIsNotNone(new_snippet)
        self.assertNotEqual(snippet.id, new_snippet.id)

        new_title = 'Updated code'
        new_code = 'print("Hi, World!")'
        new_snippet.title = new_title
        new_snippet.code = new_code
        serializer = SnippetSerializer(new_snippet)
        new_content = JSONRenderer().render(serializer.data)
        stream = BytesIO(new_content)
        data = JSONParser().parse(stream)
        serializer = SnippetSerializer(new_snippet, data=data)
        self.assertTrue(serializer.is_valid())
        updated_snippet = serializer.save()
        self.assertEquals(updated_snippet.title, new_title)
        self.assertEquals(updated_snippet.code, new_code)


class SnippetViewTest(APITestCase):

    faker = Faker()

    snippet_count = 0

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
            snippet = Snippet(title=title, code=code, linenos=linenos, language=language, style=style)
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
