from rest_framework import serializers
from apps.news.models import NewsModel, RequestResponceAIModel


class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'

class RequestResponceAIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestResponceAIModel
        fields = '__all__'