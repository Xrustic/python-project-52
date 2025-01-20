from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class CustomChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.get_full_name()}'


class TaskForm(forms.ModelForm):
    executor = CustomChoiceField(
        queryset=get_user_model().objects.all(),
        label=_('Executor'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': _('Name')}),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': _('Description'),
                       "rows": 10, "cols": 20}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'})
        }
