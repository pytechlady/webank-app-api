from django.db import models
from django.db.models.base import Model
from rest_framework import serializers
from .models import AccountManager, User, Balance



class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6,write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric character')
        return attrs
    
    def create(self, validated_data):
        return User.object.create_user(**validated_data)
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['otp', 'email']
        
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password')
        
class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountManager
        fields = ['fullname', 'occupation', 'gender', 'account_type', 'phone_number', 'address']
        
    def create(self, validated_data):
        return AccountManager.objects.create(**validated_data)
    
class BalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Balance
        fields =["account_balance"]
        