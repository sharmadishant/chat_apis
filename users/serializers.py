from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'name',  'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], password=validated_data['password'],
                                        email=validated_data.get('email'), first_name=validated_data['first_name'])
        return user

class UserSerializer(serializers.ModelSerializer):
     isStaffAdmin = serializers.SerializerMethodField(read_only=True)

     class Meta:
         model = User
         fields = ['id', 'username', 'email', 'isStaffAdmin']


     def get_isStaffAdmin(self, obj):
         return obj.is_staff

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        try:
            attrs['username'] = attrs['email']
        except:
            pass
        data = super().validate(attrs)

        data["user"] ={"id":self.user.id,
                    "name":self.user.first_name,
                    "username":self.user.username,
                    "email":self.user.email
                    }

        return data

class AllAuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')
