from django.contrib import admin

from apps.news.models import NewsModel, RequestResponceAIModel


@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_date', 'created_at',)
    search_fields = ('title', 'news_date')
    ordering = ('-news_date',)


@admin.register(RequestResponceAIModel)
class RequestResponceAIModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'response', 'created_at',)
    search_fields = ('request', 'response')
    ordering = ('-created_at',)
