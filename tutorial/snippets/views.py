from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from tutorial.snippets.models import Snippet
from tutorial.snippets.serializers import SnippetSerializer
from tutorial.snippets.permissions import IsOwnerOrReadOnly


class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
