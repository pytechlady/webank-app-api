from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import CASCADE


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
  

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    otp = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    
    def __str__(self):
        return self.email

    # def tokens(self):
    #     pass


class AccountManager(models.Model):
    ACCOUNT_CHOICES = (
        ('Savings account', 'Savings account'),
        ('Current Account', 'Current Account'),
        ('Fixed Account', 'Fixed Account'),
    )
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Binary", "Binary"),
    )
    user_id = models.OneToOneField(User, on_delete=CASCADE)
    account_type = models.CharField(
        max_length=250, null=True, choices=ACCOUNT_CHOICES)
    fullname = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=50, null=True, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=200, null=True)
    address = models.TextField(max_length=255, null=True)
    occupation = models.CharField(max_length=200, null=True)
    account_number = models.IntegerField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.user_id}:{self.account_number}'

class Balance(models.Model):
    account_balance = models.DecimalField(max_digits=50, decimal_places=2)
    customer_account = models.ForeignKey(
        AccountManager, on_delete=CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.customer_account.account_number} - {self.customer.username}'
    
    
class TransactionHistory(models.Model):
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_manager', null=True)
    user_id = models.ForeignKey(User, null=True, on_delete=CASCADE)
    account_id = models.ForeignKey(AccountManager, null=True, on_delete=CASCADE)
    balance_id = models.ForeignKey(Balance, null=True, on_delete=CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=250)
    transaction_amount = models.DecimalField(max_digits=50, decimal_places=2)
    current_balance = models.DecimalField(max_digits=50, default=0, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.user_id.id} -  {self.account_id.account_number} - {self.user_id.username}'
    
    