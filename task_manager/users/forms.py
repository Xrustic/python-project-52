from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm
)


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Фамилия'}))
    username = forms.CharField(label='Имя пользователя', required=True,
                               max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Имя пользователя'}),
                               help_text='Обязательное поле. '
                               'Не более 150 символов. Только буквы, цифры и '
                               'символы @/./+/-/_.')
    password1 = forms.CharField(label='Пароль', min_length=3, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Пароль'}),
                                help_text='Ваш пароль должен содержать как '
                                'минимум 3 символа.')
    password2 = forms.CharField(label='Повторите пароль', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Пароль'}),
                                help_text='Для подтверждения введите, '
                                'пожалуйста, пароль ещё раз.')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Фамилия'}))
    username = forms.CharField(label='Имя пользователя', required=True,
                               max_length=150,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Имя пользователя'}),
                               help_text='Обязательное поле. '
                               'Не более 150 символов. Только буквы, цифры и '
                               'символы @/./+/-/_.')
    password1 = forms.CharField(label='Пароль', min_length=3, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Пароль'}),
                                help_text='Ваш пароль должен содержать как '
                                'минимум 3 символа.')
    password2 = forms.CharField(label='Повторите пароль', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Пароль'}),
                                help_text='Для подтверждения введите, '
                                'пожалуйста, пароль ещё раз.')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
