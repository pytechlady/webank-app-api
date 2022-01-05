from django.contrib import admin
from .models import User, AccountManager

# Register your models here.
admin.site.register(User)
admin.site.register(AccountManager)
