from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.deletion import CASCADE



# Create your models here.
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
    is_verified= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    object = UserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        pass

class AccountManager(models.Model):
    ACCOUNT_CHOICES=(
        ('Savings account', 'Savings account'),
        ('Current Account', 'Current Account'),
        ('Fixed Account', 'Fixed Account'),
    )
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Binary", "Binary"),
    )
    user_id = models.ForeignKey(User, on_delete=CASCADE, unique=True)
    account_type = models.CharField(max_length=250, null=True, choices=ACCOUNT_CHOICES)
    fullname = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=50, null=True, choices=GENDER_CHOICES)
    phone_number = models.IntegerField(null=True)
    address = models.TextField(max_length=255, null=True )
    occupation = models.CharField(max_length=200, null=True)
    account_number = models.IntegerField(null=True)