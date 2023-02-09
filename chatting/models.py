from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Room(models.Model):
    USER_ROLE = (
        ("A", 'ADMIN'),
        ("U", 'USER'),
    )
    name = models.CharField(max_length=128)
    user_role = models.CharField(choices=USER_ROLE, default="U", max_length=10)
    username = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="User1") #user 1
    
    last_modified = models.DateTimeField(auto_now_add=False,blank=True,null=True)

    def __str__(self):
        return f'{self.name} {self.username} [{self.last_modified}]'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

class RoomUsers(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    room_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_user')
    is_blocked = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now_add=False,blank=True,null=True)

    def __str__(self):
        return f'{self.room_user} -- {self.room}'

    class Meta:
        ordering = ('last_modified',)