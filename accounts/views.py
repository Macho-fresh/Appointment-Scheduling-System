from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from .models import User
from django.contrib.auth import login, authenticate

# class GiveProviderView(APIView):
#     permission_classes = [IsAdminUser, IsAuthenticated]
#     def post(self, request):
#         provider_id = request.data.get('provider_id')
#         User.objects.get(id=id).is_provider = True
#         user = User.objects.get(id=id)
#         return Response({
#             'message': f'{user.username} has been promoted'
#         })

class Provider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_provider == True

class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'user already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username = username,
            email= email,
            password = password
        )

        return Response({
            'message': 'user created successfully',
            'user': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)

class RegisterProviderView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'user already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username = username,
            email= email,
            password = password,
            is_provider = True
        )

        return Response({
            'message': 'user provider created successfully',
            'user': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = []
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

