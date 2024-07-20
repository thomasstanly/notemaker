from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Note


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.name
        token['is_superuser'] = user.is_superuser
        token['first_name'] = user.first_name
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=30, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','password2','phone_number']

    def validate(self,attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError('password dosn\'t match')
        
        phone_number = attrs.get('phone_number','')
        if len(str(phone_number))!= 10:
            raise serializers.ValidationError('Phone number is not valid')
        
        if not str(phone_number).isdigit():
            raise serializers.ValidationError('Phone number should contain only digits')
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    username= serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)
    access_token= serializers.CharField(max_length=500, read_only=True)
    refresh_token= serializers.CharField(max_length=500, read_only=True)
    isAdmin = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = User
        fields = ['username','password','access_token','refresh_token','isAdmin','first_name']
    
    def validate(self,attrs):
        username= attrs.get('username')
        password= attrs.get('password')
        request = self.context.get('request')
        user= authenticate(request,username=username,password=password)
        
        if not user:
            raise AuthenticationFailed('invalid credential try again')
        token=user.tokens()

        return {
            'email':user.username,
            'isAdmin':user.is_superuser,
            'first_name':user.first_name,
            'access_token':str(token.get('access')),
            'refresh_token':str(token.get('refresh')),
        }
    
class NoteSerializers(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'user']
        read_only_fields = ['user']