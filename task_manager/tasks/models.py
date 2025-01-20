from django.db import models
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False, blank=False,
        verbose_name=_('Name'),
    )
    description = models.CharField(verbose_name=_('Description'),
                                   unique=False,
                                   null=True, blank=True,
                                   max_length=150)
    status = models.ForeignKey(Statuses,
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'), unique=False,
                               related_name='tasks')
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                               related_name='tasks_author')
    executor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 related_name='tasks_executor')
    labels = models.ManyToManyField(Label, verbose_name=_('Labels'),
                                    related_name='tasks',
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
