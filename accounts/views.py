from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import User
from django.contrib.auth import login, authenticate


class Provider(BasePermission):
    def has_permissions(self, request, view):
        return request.user.is_authenticated and request.user.is_provider

class RegisterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def create(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'user already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            username = username,
            email= email,
            pasword = password
        )

        return Response({
            'message': 'user created successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not User.objects.filter(username=username).exists():
                return Response({
                    'error': 'user does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        login(request, user)

        return Response({
            'message' : f'welcome, {username}'
        },  status=status.HTTP_202_ACCEPTED)

