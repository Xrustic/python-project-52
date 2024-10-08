from django.test import TestCase, override_settings
from ..forms import UserCreateForm
import os
import yaml


@override_settings(
    SECRET_KEY='fake-key'
)
class UserCreateFormTest(TestCase):
    def setUp(self):
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    'fixtures', 'forms.yaml'
                ),
                'r') as file:
            self.form_data = yaml.safe_load(file)

    def test_valid_data(self):
        form = UserCreateForm(self.form_data.get('user1'))
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserCreateForm(self.form_data.get('user2'))
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['username'])
        self.assertEqual(len(form.errors), 1)

    def test_invalid_password(self):
        form = UserCreateForm(self.form_data.get('user3'))
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['password2'])
        self.assertEqual(len(form.errors), 1)

    def test_no_data(self):
        form = UserCreateForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)
