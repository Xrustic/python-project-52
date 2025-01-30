from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
import os
import yaml


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class UsersViewTestMixin(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.users_url = reverse('users')
        self.user_create_url = reverse('user_create')
        self.users = auth.get_user_model().objects
        self.test_user = self.users.get(username='max_payne')
        self.test_user2 = self.users.get(username='Hermione')
        self.user_update_url = reverse('users')
        self.user1_update_url = reverse('user_update',
                                        kwargs={'pk': self.test_user.id})
        self.user2_update_url = reverse('user_update',
                                        kwargs={'pk': self.test_user2.id})
        self.user_delete_url = reverse('user_delete',
                                       kwargs={'pk': self.test_user.id})
        self.user2_delete_url = reverse('user_delete',
                                        kwargs={'pk': self.test_user2.id})


class UserCreateFormTestMixin(TestCase):

    def setUp(self):
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    'fixtures', 'forms.yaml'
                ),
                'r') as file:
            self.form_data = yaml.safe_load(file)
