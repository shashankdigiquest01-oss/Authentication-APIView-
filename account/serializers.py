from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChatBotModel ,ProfileModel

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5 )
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'username', 'email', 'password']
        fields = ['first_name', 'username', 'email', 'password']
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            # last_name=validated_data.get('last_name', ''),
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChatBotModel
        fields="__all__"
        
class ProfileSerilzer(serializers.ModelSerializer):
    profile_pic=serializers.ImageField(required=False)
    class Meta:
        model= ProfileModel
        fields = ['profile_pic']  
        
        
        
        
        