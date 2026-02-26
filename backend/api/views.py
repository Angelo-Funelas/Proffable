from django.shortcuts import render

# Import the things to function 
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from social_django.utils import load_strategy, load_backend
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

import os

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

# POST request for making a new user 
@api_view(["POST"])
def register_user(request):
    data = request.data
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        f_name=data.get("f_name", ""),
        l_name=data.get("l_name", "")
    )

    
    return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
@api_view(["POST"])
def google_login(request):
    id_token = request.data.get("id_token")
    if not id_token:
        return Response({"error": "No id_token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = jwt.decode(id_token, options={"verify_signature": False})
        #if payload.get("aud") != GOOGLE_CLIENT_ID:
        #    return Response({"error": "Invalid client"}, status=status.HTTP_400_BAD_REQUEST)

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