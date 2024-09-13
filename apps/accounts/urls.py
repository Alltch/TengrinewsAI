from django.urls import path
from apps.accounts.views import CreateTokenView

urlpatterns = [
    path('create-token/', CreateTokenView.as_view(), name='create-token'),
]