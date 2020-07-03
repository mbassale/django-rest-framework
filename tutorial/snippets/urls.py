from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tutorial.snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
