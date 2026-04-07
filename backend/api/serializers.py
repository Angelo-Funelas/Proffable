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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "f_name", "m_name", "l_name", "profile_picture_url", "is_moderator"]

class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ["username", "email", "f_name", "m_name", "l_name", "profile_picture_url", "password", "current_password",]

    def validate(self, attrs):
        password = attrs.get("password")
        current_password = attrs.get("current_password")
        user = self.instance

        if password:
            if user.has_usable_password():
                if not current_password:
                    raise serializers.ValidationError({
                        "current_password": "Current password is required."
                    })

                if not user.check_password(current_password):
                    raise serializers.ValidationError({
                        "current_password": "Current password is incorrect."
                    })

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("current_password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance