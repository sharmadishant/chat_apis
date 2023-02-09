from django.contrib.auth.models import User
from rest_framework import serializers
from chatting.models import *

class AllAuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','username', 'user_role',)

class UserInRoomSerializer(serializers.ModelSerializer):
    room_user = AllAuthUserSerializer()
    class Meta:
        model = RoomUsers
        fields = ('room_user',)