import imp
from django.urls import path

from webank.models import TransactionHistory
from webank.views.transactions import Transactions, Transaction
from webank.views.users import OneUser, Users
from .views.create_account_view import AccountView
from .views.delete_views import DeleteAcount, DeactiveAccount, ActivateAccount
from .views.verify_email_views import VerifyEmail
from .views.registerviews import RegisterView, RegisterAdminView
from .views.loginview import LoginView, LogoutView
from .views.fund_account import DebitBalance, CreditBalance
from .views.forgot_password import ForgotPasswordView, PasswordReset
from .views.accounts import Accounts, Account


urlpatterns = [
   path('register', RegisterView.as_view(), name='register'),
   path('email-verify', VerifyEmail.as_view(), name='email-verify'),
   path('login', LoginView.as_view(), name='login'),
   path('create-account', AccountView.as_view(), name='create-account'),
   path('delete/<int:pk>', DeleteAcount.as_view(), name='delete'),
   path('register-admin', RegisterAdminView.as_view(), name='register-admin'),
   path('credit-account', 
        CreditBalance.as_view(), name='credit-account'),
   path('debit-account', 
        DebitBalance.as_view(), name='debit-account'),
   path('deactivate/<int:pk>', DeactiveAccount.as_view(), name='deactivate'),
   path('activate/<int:pk>', ActivateAccount.as_view(), name='activate'),
   path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
   path('reset-password', PasswordReset.as_view(), name='reset-password'),
   path('logout', LogoutView.as_view(), name='logout'),
   path('accounts', Accounts.as_view(), name='accounts'),
   path('account/<int:pk>', Account.as_view(), name='account'),
   path('users', Users.as_view(), name='users'),
   path('user/<int:pk>', OneUser.as_view(), name='user'),
   path('transactions', Transactions.as_view(), name='transactions'),
   path('transaction/<int:pk>', Transaction.as_view(), name='transaction'),
]