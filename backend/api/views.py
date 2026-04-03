from django.shortcuts import render

# Import the things to function 
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from social_django.utils import load_strategy, load_backend
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .serializers import UsernameOrEmailTokenSerializer, ProfileSerializer, UpdateProfileSerializer

import os

User = get_user_model()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

# Entity User
from api.models import User

# Conver to JSON
from .serializers import RegisterSerializer

# GET request for user information
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "email": user.email,
        "f_name": user.f_name,
        "l_name": user.l_name,
        "is_moderator": user.is_moderator,
    })

@api_view(["POST"])
def register_user(request):
    data = request.data
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    f_name = data.get("f_name", "")
    l_name = data.get("l_name", "")

    # Check required fields
    if not email or not username or not password:
        return Response(
            {"error": "Username, email, and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for duplicate email
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for duplicate username
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        f_name=f_name,
        l_name=l_name
    )

    return Response(
        {"message": "User created successfully."},
        status=status.HTTP_201_CREATED
    )

class LoginView(TokenObtainPairView):
    serializer_class = UsernameOrEmailTokenSerializer 
    
@api_view(["POST"])
def google_login(request):
    token = request.data.get("token")
    if not token:
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # id_info = id_token.verify_oauth2_token(
        #     token, 
        #     google_requests.Request(), 
        #     settings.GOOGLE_OAUTH_CLIENT_ID
        # )
        payload = jwt.decode(token, options={"verify_signature": False})
        #if payload.get("aud") != GOOGLE_CLIENT_ID:
        #    return Response({"error": "Invalid client"}, status=status.HTTP_400_BAD_REQUEST)

        # email = id_info['email']
        # f_name = id_info.get('given_name', '')
        # last_name = id_info.get('family_name', '')
        # l_name = id_info.get('picture', '')

        email = payload.get("email")
        f_name = payload.get("given_name", "")
        l_name = payload.get("family_name", "")

        random_password = get_random_string(length=12)  
        hashed_password = make_password(random_password)

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "f_name": f_name,
                "l_name": l_name,
                "password": hashed_password,
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)

# Update user profile
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)