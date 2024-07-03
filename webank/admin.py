from django.contrib import admin
from .models import Balance, User, AccountManager, TransactionHistory


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 
                    'is_verified', 'is_active', 'is_staff', 'updated_at')
    list_display_links = ('id', 'email', 'username')

   
admin.site.register(User, UserAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'account_type', 'gender', 'account_number', 'created_at')
    
    list_display_links = ('user_id', 'account_type', 'account_number')
    
admin.site.register(AccountManager, AccountAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_balance', 'customer_account', 'customer')
    list_display_links = ('id', 'account_balance')
    
admin.site.register(Balance, BalanceAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_amount', 'account_id')
    list_display_links = ('id', 'transaction_amount')
    
admin.site.register(TransactionHistory, TransactionAdmin)

