from django.contrib import admin
from .models import Balance, User, AccountManager


# Register your models here.
admin.site.register(AccountManager)
admin.site.register(Balance)


class DisplayAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 
                    'is_verified', 'is_active', 'is_staff', 'updated_at')
    list_display_links = ('id', 'email', 'username')

   
admin.site.register(User, DisplayAdmin)
