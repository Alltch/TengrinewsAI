from django.urls import path
from apps.news.views import start_scraper

urlpatterns = [
    path('', start_scraper, name='start_scraper'),
]