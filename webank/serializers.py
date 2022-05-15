from rest_framework import serializers
from .models import AccountManager, User, Balance, TransactionHistory


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length = 68, min_length = 6, write_only = True)

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
        return User.objects.create_user(**validated_data)
    

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
        
class LogoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields =['email', 'password']
        

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountManager
        fields = [
            'fullname', 'occupation', 'gender', 'account_type', 
            'phone_number', 'address']
  
    def create(self, validated_data):
        return AccountManager.objects.create(**validated_data)
    

class BalanceSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=100, decimal_places=3)
    account_number = serializers.CharField()
    class Meta:
        model = AccountManager
        fields = ("account_number", "amount")
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
        
class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('email',)
        
class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=2)
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    class Meta:
        fields=['email','otp','password','confirm_password']
        
        
class CreditBalanceSerializer(serializers.ModelSerializer):
    account_number = serializers.IntegerField()
    class Meta:
        model = Balance
        fields = ['account_number', 'credit_amount']
        
        
class DebitBalanceSerializer(serializers.ModelSerializer):
    account_number = serializers.IntegerField()
    class Meta:
        model = Balance
        fields = ['account_number', 'debit_amount']
        
        
class ManageAccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username']
        
        
class AccountViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountManager
        fields = ['user_id', 'fullname', 'account_number', 'account_type', 'occupation', 'address', 'phone_number']
        
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['user_id', 'account_id', 'balance_id', 'transaction_type', 'transaction_amount', 'transaction_time']
        

