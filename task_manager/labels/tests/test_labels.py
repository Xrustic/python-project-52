from django.test import TestCase
from django.contrib import auth
from django.urls import reverse, resolve
from ..views import (
    LabelIndexView,
    LabelCreateView,
    LabelDeleteView,
    LabelUpdateView
)
from task_manager.labels.forms import LabelForm
from .mixins import (
    LabelsCreationFormTestMixin,
    LabelsViewsTestMixin
)


class LabelsCreationFormTest(LabelsCreationFormTestMixin, TestCase):

    def test_creation_form_with_valid_data(self):
        form = LabelForm(self.form_data.get('status1'))
        self.assertTrue(form.is_valid())

    def test_creation_form_with_invalid_data(self):
        form = LabelForm(self.form_data.get('status2'))
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['name'])
        self.assertEqual(len(form.errors), 1)

    def test_creation_form_with_no_data(self):
        form = LabelForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class LabelUrlsTest(TestCase):
    def test_label_index_url(self):
        url = reverse('labels')
        self.assertEqual(resolve(url).func.view_class, LabelIndexView)

    def test_label_create_url(self):
        url = reverse('labels_create')
        self.assertEqual(resolve(url).func.view_class, LabelCreateView)

    def test_label_update_url(self):
        url = reverse('labels_update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, LabelUpdateView)

    def test_label_delete_url(self):
        url = reverse('labels_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, LabelDeleteView)


class LabelsViewsTest(LabelsViewsTestMixin, TestCase):
    fixtures = ['labels', 'users']

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
