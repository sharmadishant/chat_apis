from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=300, null=True, blank=True)
    phone_no = models.IntegerField(null=True,blank=True)
    username = models.CharField(max_length=255, null=True, unique=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to='Profiles/',default='Profiles/user-default.png')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


        