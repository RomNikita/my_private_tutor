from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('name', 'surname', 'date_of_birthday', 'phone', 'password1', 'password2', 'avatar')
