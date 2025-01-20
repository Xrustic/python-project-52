from django import forms
from .models import Statuses
from django.utils.translation import gettext_lazy as _


class StatusForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True,
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': _('Name')}))

    class Meta:
        model = Statuses
        fields = ['name']
