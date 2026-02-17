from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class User(AbstractUser):
    # institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, related_name="students") uncomment once Institution model is created
    f_name = models.CharField(blank="False", max_length=32)
    l_name = models.CharField(blank="False", max_length=32)
    m_name = models.CharField(blank="True", max_length=32)
    profile_picture_url = models.CharField(blank="True", max_length=128)
    is_moderator = models.BooleanField(default=False)
    email = models.EmailField(unique=True, max_length=254)
    objects = CustomUserManager()
    def __str__(self):
        return f"{self.l_name} @ {self.email}"