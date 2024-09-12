from datetime import datetime, time

from openai import OpenAI

from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.request import Request

from apps.news.parse import NewsParser
from apps.news.serializers import NewsModelSerializer, RequestResponceAIModelSerializer
from apps.news.models import NewsModel, RequestResponceAIModel



def start_scraper(request):
    parser = NewsParser(url='https://tengrinews.kz/')
    parser.processing()
    return HttpResponse("Scraping completed successfully!")


def request_ai(prompt):
    client = OpenAI(api_key=settings.API_KEY)
    model = "gpt-4o"

    message = {"role": "user", "content": prompt}

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": settings.SYSTEM_TEXT},
            message
        ]
    )

    return completion.choices[0].message.content


class NewsListCreateApiView(generics.ListCreateAPIView):
    queryset = NewsModel.objects.all()
    serializer_class = NewsModelSerializer
    permission_classes = [permissions.IsAdminUser]


class NewsModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsModel.objects.all()
    serializer_class = NewsModelSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


class RequestResponceAIModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = RequestResponceAIModel.objects.all()
    serializer_class = RequestResponceAIModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request: Request, *args, **kwargs):
        # Query the news data
        data = NewsModel.objects.filter(news_date__date=datetime.now().date()).order_by('-news_date')
        text = ",\n".join([f"{nm.title} - {nm.news_date}" for nm in data])

        # Get AI response
        output_ai = request_ai(prompt=text + request.data.get('request', ''))

        # Create a mutable copy of request.data
        mutable_data = request.data.copy()
        mutable_data['response'] = output_ai

        # Update the request to use the mutable data
        request._full_data = mutable_data

        return super().post(request, *args, **kwargs)
    

class RequestResponceAIModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RequestResponceAIModel.objects.all()
    serializer_class = RequestResponceAIModelSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
