from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView, AccountView, DeleteAcount, RegisterAdminView, CreditBalance, DebitBalance, DeactiveAccount, ActivateAccount


urlpatterns = [
   path('register', RegisterView.as_view(), name = 'register'),
   path('email-verify', VerifyEmail.as_view(), name = 'email-verify'),
   path('login', LoginView.as_view(), name='login'),
   path('create-account', AccountView.as_view(), name='create-account'),
   path('delete/<int:pk>', DeleteAcount.as_view(), name='delete'),
   path('register-admin', RegisterAdminView.as_view(), name='register-admin'),
   path('credit-account/<int:pk>', CreditBalance.as_view(), name='credit-account'),
   path('debit-account/<int:pk>', DebitBalance.as_view(), name='debit-account'),
   path('deactivate/<int:pk>', DeactiveAccount.as_view(), name='deactivate'),
   path('activate/<int:pk>', ActivateAccount.as_view(), name='activate'),
]