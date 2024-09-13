from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CreateTokenView(APIView):
    permission_classes = [AllowAny]  # Доступ разрешён для всех

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if user:
            # Получение или создание токена
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)