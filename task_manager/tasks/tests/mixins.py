from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
from task_manager.settings import LOGIN_URL
from task_manager.tasks.models import Task
import os
import yaml


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class TaskViewsTestMixin(TestCase):
    fixtures = ['users', 'labels', 'statuses', 'tasks']

    def setUp(self):
        self.client = Client()
        self.tasks = Task.objects
        self.users_model = auth.get_user_model()
        self.user = self.users_model.objects.get(pk=1)
        self.user2 = self.users_model.objects.get(pk=2)
        self.login_url = reverse(LOGIN_URL)
        self.task_create_url = reverse('task_create')
        self.task_view_url = reverse('task_detail', kwargs={'pk': 1})
        self.task_update_url1 = reverse('task_update', kwargs={'pk': 1})
        self.task_update_url2 = reverse('task_update', kwargs={'pk': 2})
        self.task_delete_url1 = reverse('task_delete', kwargs={'pk': 1})
        self.task_delete_url2 = reverse('task_delete', kwargs={'pk': 2})
        self.tasks_url = reverse('tasks')


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class TaskCreationFormTestMixin(TestCase):
    fixtures = ['users', 'statuses']

    def setUp(self):
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    'fixtures', 'forms.yaml'
                ),
                'r') as file:
            self.form_data = yaml.safe_load(file)
