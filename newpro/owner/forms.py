from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser

from crispy_forms.helper import FormHelper


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def clean(self):
        username = self.cleaned_data.get('username')

        if username[0].isupper():
            raise ValidationError('Usernames should start with small letters.')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


    def clean(self):
        username = self.cleaned_data.get('username')

        if username[0].isupper():
            raise ValidationError('Usernames should start with small letters.')

