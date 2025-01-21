from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm
)
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class CustomUserChangeForm(CustomUserCreationForm):

    def clean_username(self):
        return self.cleaned_data.get("username")


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label=_('Name'), required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': _('Name')}))
    last_name = forms.CharField(label=_('Surname'), required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Surname')}))
    username = forms.CharField(label=_('User name'), required=True,
                               max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('User name')}),
                               help_text=_('Required field. No more than 150 '
                                           'characters. Only letters, '
                                           'numbers and symbols @/./+/-/_.'))
    password1 = forms.CharField(label=_('Password'), min_length=3, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Password')}),
                                help_text=_('Your password must contain at least '
                                            '3 characters.'))
    password2 = forms.CharField(label=_('Password confirmation'), required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Password confirmation')}),
                                help_text=_('To confirm, please enter your '
                                            'password again.'))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': _('Name'),
            'last_name': _('Surname'),
            'username': _('User name'),
        }


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(label=_('Name'), required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': _('Name')}))
    last_name = forms.CharField(label=_('Surname'), required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Surname')}))
    username = forms.CharField(label=_('User name'), required=True,
                               max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('User name')}),
                               help_text=_('Required field. No more than 150 characters. '
                                           'Only letters, numbers and symbols '
                                           '@/./+/-/_.'))
    password1 = forms.CharField(label=_('Password'), min_length=3, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Password')}),
                                help_text=_('Your password must contain at least '
                                            '3 characters.'))
    password2 = forms.CharField(label=_('Password confirmation'), required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Password confirmation')}),
                                help_text=_('To confirm, please enter your '
                                            'password again.'))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': _('Name'),
            'last_name': _('Surname'),
            'username': _('User name'),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label=_('User name'),
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': _('User name')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password')}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
