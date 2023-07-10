from django.contrib import admin
from .models import Balance, User, AccountManager, TransactionHistory


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 
                    'is_verified', 'is_active', 'is_staff', 'updated_at')
    list_display_links = ('id', 'email', 'username')

   
admin.site.register(User, UserAdmin)
admin.site.register(AccountManager)
admin.site.register(Balance)
admin.site.register(TransactionHistory)

