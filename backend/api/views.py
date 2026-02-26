from django.shortcuts import render

# Import the things to function 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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