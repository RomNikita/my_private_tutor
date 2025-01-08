from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import UserCreateView, SuccessRegistrationView

app_name = 'users'

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('registration/success/', SuccessRegistrationView.as_view(), name='registration_success'),
    path('login/', LoginView.as_view(template_name='user_login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='user_logout.html'), name='logout'),
]
