from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NewsModel(BaseModel):
    title = models.CharField(max_length=255)
    news_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'



class RequestResponceAIModel(BaseModel):
    request = models.TextField(max_length=500)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.request

    class Meta:
        verbose_name = 'RequestResponseAI'
        verbose_name_plural = 'RequestResponseAI'
        ordering = ['-created_at']
