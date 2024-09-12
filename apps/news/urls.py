from django.urls import path
from apps.news.views import start_scraper

from apps.news.views import (
    NewsListCreateApiView,
    NewsModelRetrieveUpdateDestroyAPIView,
    RequestResponceAIModelListCreateAPIView,
    RequestResponceAIModelRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('', start_scraper, name='start_scraper'),
    path('news/', NewsListCreateApiView.as_view(), name='news_list_create'),
    path('news/<int:pk>/', NewsModelRetrieveUpdateDestroyAPIView.as_view(), name='news_retrieve_update_destroy'),
    path('request-response-ai/', RequestResponceAIModelListCreateAPIView.as_view(), name='request_response_ai_list_create'),
    path('request-response-ai/<int:pk>/', RequestResponceAIModelRetrieveUpdateDestroyAPIView.as_view(), name='request_response_ai_retrieve_update_destroy'),
]