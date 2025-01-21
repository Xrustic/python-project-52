from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
from task_manager.labels.models import Label
import os


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class LabelsViewsTest(TestCase):
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

    def test_auth_user_label_index(self):
        self.client.force_login(self.user)
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_anonym_user_label_index(self):
        response = self.client.get(self.labels_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_label_create_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.label_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_anonym_user_label_create_GET(self):
        response = self.client.get(self.label_create_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_label_create_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_create_url,
                                    {"name": "new_label1"})
        self.assertEqual(self.labels.get(name='new_label1').name, 'new_label1')
        self.assertEqual(self.labels.count(), 3)
        self.assertRedirects(response, self.labels_url)

    def test_auth_user_label_create_no_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_create_url)
        self.assertEqual(response.status_code, 200)

    def test_auth_user_label_create_exist_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_create_url, {"name": "label1"})
        self.assertEqual(response.status_code, 302)

    def test_anonym_user_label_create_POST(self):
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_create_url,
                                    {"name": "new_status1"})
        self.assertEqual(self.labels.count(), 2)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_label_update_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.label_update_url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/update.html')

    def test_anonym_user_label_update_GET(self):
        response = self.client.get(self.label_update_url1)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_label_update_success_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_update_url1,
                                    {"name": "updated1"})
        self.assertEqual(self.labels.count(), 2)
        self.assertEqual(self.labels.get(name="updated1").name, "updated1")
        self.assertRedirects(response, self.labels_url)

    def test_auth_user_label_update_fail_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(self.label_update_url1, {"name": ""})
        self.assertEqual(self.labels.get(name="label1").name, "label1")
        self.assertEqual(response.status_code, 200)

    def test_anonym_user_label_update_POST(self):
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_update_url1,
                                    {"name": "updated1"})
        self.assertEqual(self.labels.filter(name="updated1").count(), 0)
        self.assertEqual(self.labels.count(), 2)
        self.assertRedirects(response, self.login_url)

    def test_auth_another_label_update_POST(self):
        self.client.force_login(self.user)
        self.client.post(self.label_create_url, {"name": "created1"})
        new_label = self.labels.get(name="created1")
        self.label_update_url3 = reverse('labels_update',
                                         kwargs={'pk': new_label.pk})
        self.assertEqual(self.labels.filter(name="created1").count(), 1)
        self.client.logout()
        self.assertEqual(auth.get_user(self.client).is_authenticated, False)
        self.client.force_login(self.user2)
        response = self.client.post(self.label_update_url3,
                                    {"name": "updated2"})
        self.assertEqual(self.labels.get(name="updated2").name, 'updated2')
        self.assertEqual(self.labels.filter(name='created1').count(), 0)
        self.assertRedirects(response, self.labels_url)

    def test_auth_user_label_delete_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.label_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/delete.html')

    def test_anonym_user_label_delete_GET(self):
        response = self.client.get(self.label_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_label_delete_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_delete_url)
        self.assertEqual(self.labels.count(), 1)
        self.assertRedirects(response, self.labels_url)

    def test_anonym_user_label_delete_POST(self):
        self.assertEqual(self.labels.count(), 2)
        response = self.client.post(self.label_delete_url)
        self.assertEqual(self.labels.count(), 2)
        self.assertRedirects(response, self.login_url)
