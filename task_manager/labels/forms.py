from django import forms
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True,
                           max_length=100,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': _('Name')}))

    class Meta:
        model = Label
        fields = ['name']
