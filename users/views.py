from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

import json
from .serializers import *
# ---------------- API 's -------------------
class createUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("data serializer start")
        print(serializer.is_valid())
        print("data serializer end")
        # print(serializer.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            return Response({
               "user": UserSerializer(user, context=self.get_serializer_context()).data,
            })
        except Exception as e:
            return Response({"msg": f"This email address is already registered with us"},
                            status=status.HTTP_409_CONFLICT)

class loginPage(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, format=None):
        data = request.data
        
        try:
            data['username'] = data['email']
        except:
            pass
        serializer = AuthTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        login(request, user)
        return_data = super(loginPage, self).post(request, format=None)

        return_data.data['token']= return_data.data['access']
        del return_data.data['access']
        return return_data

def logoutUser(request):
    messages.info(request, "User logout successfully")

    logout(request)
    return Response({ "success": "ok" })

class UserUpdateApiView(generics.ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def patch(self, request, *args, **kwargs):
        try: 
            user =  request.user
            user_info = User.objects.get(id = user.id)                
            print(user_info)
            serializer = AllAuthUserSerializer(user_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                log = json.loads(json.dumps(serializer.data))
                print(log)
                return Response({'msg':'data Updates','data':log}, status=status.HTTP_201_CREATED)
            return Response({"msg": "No Content"},status=204)
        except Exception as ex:
                return Response({"error": str(ex)},status=400)