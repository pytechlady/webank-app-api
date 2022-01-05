from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView, AccountView


urlpatterns = [
   path('register', RegisterView.as_view(), name = 'register'),
   path('email-verify', VerifyEmail.as_view(), name = 'email-verify'),
   path('login', LoginView.as_view(), name='login'),
   path('create-account', AccountView.as_view(), name='create-account')
]