from .models import AccountManager, User, Balance
from rest_framework import generics, serializers, status
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, AccountSerializer, BalanceSerializer
from rest_framework.response import Response
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin



    
class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.object.get(email=user_data['email'])
        user_data = serializer.data
        otp = Util.generate_otp(6)
        user.otp = otp
        user.save()
        current_site = get_current_site(request).domain
    
       
        absurl = 'http://'+current_site+'?otp='+str(otp)
        email_body = 'Hi '+user.username+' Use link below to verify ypur email \n'+ absurl
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class RegisterAdminView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.object.get(email=user_data['email'])
        user_data = serializer.data
        otp = Util.generate_otp(6)
        user.otp = otp
        user.is_staff = True
        user.save()
 
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    
    def post(self, request):
        data = request.data
        otp = data.get('otp', '')
        email = data.get('email', '')
        if otp is None or email is None:
            return Response(data=dict(invalid_input="Please provide both otp and email"), status=status.HTTP_400_BAD_REQUEST)
        get_user = User.object.filter(email=email)
        if not get_user.exists():
            return Response(data=dict(invalid_email = "please provide a valid registered email"), status=status.HTTP_400_BAD_REQUEST )
        user = get_user[0] 
        if user.otp != otp:
            return Response(data=dict(invalid_otp = "please provide a valid otp code"), status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
       
        user.save()
        return Response(data={
                "verified status":"Your account has been successfully verified"
            }, status=status.HTTP_200_OK)
        
class LoginView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        if email is None or password is None:
            return Response(data={'invalid_credentials': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response(data={'invalid_credentials': 'Ensure both email and password are correct and you have verify you account'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response(data={'invalid_credentials': 'Please verify your account'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key,}, status=status.HTTP_200_OK)
    
class AccountView(generics.GenericAPIView):
    
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id  = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            fullname =serializer.validated_data.get('fullname')
            account_type = AccountManager.objects.values_list('account_type', flat=True).distinct()
            account_number = Util.generate_account_number()
            phone_number = serializer.validated_data.get('phone_number')
            gender = AccountManager.objects.values_list('gender', flat=True).distinct()
            occupation = serializer.validated_data.get('occupation')
            address =serializer.validated_data.get('address')
            try:
                account = AccountManager.objects.create(
                    user_id = user_id,
                    fullname = fullname,
                    account_type = account_type,
                    account_number = account_number,
                    phone_number = phone_number,
                    gender = gender,
                    occupation = occupation,
                    address = address,
                )
                
                return Response({"success": f"account succesfully created, your account number is {account.account_number}"}, status=status.HTTP_206_PARTIAL_CONTENT)
                
            except:
                return Response({'error': 'You already have an account'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAcount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    queryset = User.object.all()
    
    def delete(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.delete()
            return Response({'data':"user successfully deleted"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST)
        
        
    

class CreditBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.object.get(pk = pk)
        balance = Balance.objects.filter(customer=user).first()
        if balance:
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance += credit_or_debit
            balance.save()
            return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
        else:
            account = AccountManager.objects.get(user_id = user)
            balance = Balance.objects.create(
                customer = user,
                customer_account = account,
                account_balance = 0
            )
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance += credit_or_debit
            balance.save()
            return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
        
class DebitBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.object.get(pk = pk)
        balance = Balance.objects.filter(customer=user).first()
        if balance:
            credit_or_debit = serializer.validated_data.get('account_balance')
            if balance.account_balance >= credit_or_debit:
                balance.account_balance -= credit_or_debit
                balance.save()
                return Response({"success": f'account debited sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
            else:
                balance.account_balance = balance.account_balance
                balance.save()
                return Response({'Error': f'Insuffient funds. Your account balance is {balance.account_balance}'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            account = AccountManager.objects.get(user_id = user)
            balance = Balance.objects.create(
                customer = user,
                customer_account = account,
                account_balance = 0
            )
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance = balance.account_balance
            balance.save()
            return Response({"Error": f'Insufficient fund, kindly credit your account'}, status=status.HTTP_402_PAYMENT_REQUIRED)
     
    
class DeactiveAccount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    
    queryset = User.object.all()
    
    def post(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.is_verified = False
            user_account.save()
            return Response({'data':"user successfully deactivated"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST)
        
class ActivateAccount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    
    queryset = User.object.all()
    
    def post(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.is_verified = True
            user_account.save()
            return Response({'data':"user successfully activated"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST)