import django_filters
from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Statuses
from django.contrib.auth import get_user_model
from .forms import CustomChoiceField
from django.utils.translation import gettext_lazy as _


class CustomExecutorFilter(django_filters.Filter):
    field_class = CustomChoiceField


class TaskFilter(django_filters.FilterSet):
    executor = CustomExecutorFilter(
        queryset=get_user_model().objects.all(),
        label=_('Executor'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=_('Status'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    author = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={
            'class': "form-check-input mr-3"}),
        label=_("Only your tasks"),
        method="self_tasks",
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    def self_tasks(self, queryset, name, value):
        if name == 'author' and value:
            return queryset.filter(author__exact=self.request.user)
        return queryset
