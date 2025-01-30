from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
from task_manager.labels.models import Label
import os
import yaml


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class LabelsViewsTestMixin(TestCase):
    fixtures = ['labels', 'users']

    def setUp(self):
        self.client = Client()
        self.labels = Label.objects
        self.users_model = auth.get_user_model()
        self.user = self.users_model.objects.get(pk=1)
        self.user2 = self.users_model.objects.get(pk=2)
        self.login_url = reverse(settings.LOGIN_URL)
        self.label_create_url = reverse('labels_create')
        self.label_update_url1 = reverse('labels_update', kwargs={'pk': 1})
        self.label_update_url2 = reverse('labels_update', kwargs={'pk': 2})
        self.label_delete_url = reverse('labels_delete', kwargs={'pk': 1})
        self.labels_url = reverse('labels')


class LabelsCreationFormTestMixin(TestCase):

    def setUp(self):
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    'fixtures', 'forms.yaml'
                ),
                'r') as file:
            self.form_data = yaml.safe_load(file)
