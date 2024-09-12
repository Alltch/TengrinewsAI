from django.contrib import admin

from apps.news.models import NewsModel


@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_date', 'created_at',)
    search_fields = ('title', 'news_date')
    ordering = ('-news_date',)