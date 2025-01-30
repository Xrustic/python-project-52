from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
from task_manager.settings import LOGIN_URL
from task_manager.statuses.models import Statuses
import os
import yaml


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class StatusViewsTestMixin(TestCase):
    fixtures = ["statuses", "users"]

    def setUp(self):
        self.client = Client()
        self.statuses = Statuses.objects
        self.users_model = auth.get_user_model()
        self.user = self.users_model.objects.get(pk=1)
        self.user2 = self.users_model.objects.get(pk=2)
        self.login_url = reverse(LOGIN_URL)
        self.status_create_url = reverse('status_create')
        self.status_update_url1 = reverse('status_update', kwargs={'pk': 1})
        self.status_update_url2 = reverse('status_update', kwargs={'pk': 2})
        self.status_delete_url1 = reverse('status_delete', kwargs={'pk': 1})
        self.status_delete_url2 = reverse('status_delete', kwargs={'pk': 2})
        self.statuses_url = reverse('statuses')


class StatusCreationFormTestMixin(TestCase):

    def setUp(self):
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    'fixtures', 'forms.yaml'
                ),
                'r') as file:
            self.form_data = yaml.safe_load(file)
