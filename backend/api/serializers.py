from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from api.models import User 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["is_moderator"] = user.is_moderator

        return token

class UsernameOrEmailTokenSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):

        login = attrs.get("username")   # field sent from frontend
        password = attrs.get("password")

        user = None

        # Check if login looks like an email
        if "@" in login:
            try:
                user = User.objects.get(email=login)
                attrs["username"] = user.username
            except User.DoesNotExist:
                pass

        return super().validate(attrs)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "f_name", "l_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer