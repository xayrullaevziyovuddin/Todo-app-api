from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

