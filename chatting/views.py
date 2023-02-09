import json
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from chatting.models import Message, Room, RoomUsers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from chatting.serializer import UserInRoomSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
#  -------------------------------------------------------
from .serializer import *
@api_view(['POST'])
@csrf_exempt
def addUserInGroup(request):
    data = request.data
    try:
        room = Room.objects.get(username = request.user, id = data['room_id'])
        if(room.user_role == 'A'):
            userToAdd = User.objects.get(id=data['user'])
            print(request.user,userToAdd)
            RoomUsers.objects.get_or_create(room=room, room_user = userToAdd )
    except:
        return JsonResponse({'status':"false","error":"not allowed to send message"}, safe=False)

    """
    Add New User.
    """
    return JsonResponse({'status':"ok"}, safe=False)

@api_view(['DELETE'])
@csrf_exempt
def delUserInGroup(request):
    data = request.data
    try:
        room = Room.objects.get(username = request.user, id = data['room_id'])
        if(room.user_role == 'A'):
            tempStore = RoomUsers.objects.get(id = data['user'])
            tempStore.delete()
    except:
        return JsonResponse({'status':"false","error":"Admin Can remove Any Member"}, safe=False)

    """
    Remove Any User.
    """
    return JsonResponse({'status':"ok"}, safe=False)

@api_view(['GET'])
@csrf_exempt
def searchUserInGroup(request):
    """
    Search Any User.
    """
    data = request.data
    try:
        if(request.query_params.__contains__('search')):
            print( data['room_id'], )
            room = Room.objects.get(id = data['room_id'])
            tempStore = RoomUsers.objects.filter(room = room).filter(room_user__username__icontains = request.query_params['search'])
            serializer = UserInRoomSerializer(tempStore, many=True)
            return JsonResponse({"data":serializer.data})
    except:
        return JsonResponse({'status':"false","error":"No User"}, safe=False)

# @login_required(login_url='login') 
@api_view(['POST'])
@csrf_exempt
def message_sendto_db(request):
    """
    Create a new message.
    """
    data = request.data
    message = data['prompt']
    room = Room.objects.get(id= data['user[room]'])
    try:
        isUserExist = RoomUsers.objects.get(room_user= request.user)
        isUserExist.is_blocked
        print(isUserExist.is_blocked)
        if(isUserExist.is_blocked == False):
            message = Message.objects.create(sender = request.user, receiver = room, message = message )
            message.save()
    except:
        return JsonResponse({'status':"false","error":"not allowed to send message"}, safe=False)

    return JsonResponse({'status':"ok"}, safe=False)

# @login_required(login_url='login') 
@api_view(['GET'])
@csrf_exempt
def message_view(request):
    """
    List All Message. From Perticular Chat
    """
    data = request.data
    try:
        room = Room.objects.get(id = data['room'])
        isUserExist = RoomUsers.objects.get(room = room, room_user = request.user)
        isUserExist.is_blocked
        if(isUserExist.is_blocked == False):
            message = Message.objects.filter(receiver = room)
            queary = MessageSerializer(message,many=True)
            return JsonResponse({'data': queary.data}, safe=False)
    except:
        return JsonResponse({'status':"false","error":"Not Allowed to View Message"}, safe=False)

    return JsonResponse({'status':"ok"}, safe=False)