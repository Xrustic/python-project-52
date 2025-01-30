from django.contrib import auth
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (
    StatusIndexView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView
)
from task_manager.statuses.forms import StatusForm
from .mixins import (
    StatusViewsTestMixin,
    StatusCreationFormTestMixin
)


class StatusCreationFormTest(StatusCreationFormTestMixin, TestCase):
    def test_creation_form_with_valid_data(self):
        form = StatusForm(self.form_data.get('status1'))
        self.assertTrue(form.is_valid())

    def test_creation_form_with_invalid_data(self):
        form = StatusForm(self.form_data.get('status2'))
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['name'])
        self.assertEqual(len(form.errors), 1)

    def test_creation_form_with_no_data(self):
        form = StatusForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class StatusUrlsTest(TestCase):
    def test_status_index_url(self):
        url = reverse('statuses')
        self.assertEqual(resolve(url).func.view_class, StatusIndexView)

    def test_status_create_url(self):
        url = reverse('status_create')
        self.assertEqual(resolve(url).func.view_class, StatusCreateView)

    def test_status_update_url(self):
        url = reverse('status_update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, StatusUpdateView)

    def test_status_delete_url(self):
        url = reverse('status_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, StatusDeleteView)


class StatusViewsTest(StatusViewsTestMixin, TestCase):
    fixtures = ["statuses", "users"]

    def test_auth_user_status_index(self):
        self.client.force_login(self.user)
        response = self.client.get(self.statuses_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_anonym_user_status_index(self):
        response = self.client.get(self.statuses_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_status_create_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.status_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_anonym_user_status_create_GET(self):
        response = self.client.get(self.status_create_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_status_create_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_create_url,
                                    {"name": "new_status1"})
        self.assertEqual(self.statuses.get(name='new_status1').name,
                         'new_status1')
        self.assertEqual(self.statuses.count(), 3)
        self.assertRedirects(response, self.statuses_url)

    def test_auth_user_status_create_no_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_create_url)
        self.assertEqual(response.status_code, 200)

    def test_auth_user_status_create_exist_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_create_url,
                                    {"name": "Finished"})
        self.assertEqual(response.status_code, 302)

    def test_anonym_user_status_create_POST(self):
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_create_url,
                                    {"name": "new_status1"})
        self.assertEqual(self.statuses.count(), 2)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_status_update_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.status_update_url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_anonym_user_status_update_GET(self):
        response = self.client.get(self.status_update_url1)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_status_update_success_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_update_url1,
                                    {"name": "updated1"})
        self.assertEqual(self.statuses.count(), 2)
        self.assertEqual(self.statuses.get(name="updated1").name, "updated1")
        self.assertRedirects(response, self.statuses_url)

    def test_auth_user_status_update_fail_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(self.status_update_url1, {"name": ""})
        self.assertEqual(self.statuses.get(name="In progress").name,
                         "In progress")
        self.assertEqual(response.status_code, 200)

    def test_anonym_user_status_update_POST(self):
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_update_url1,
                                    {"name": "updated1"})
        self.assertEqual(self.statuses.filter(name="updated1").count(), 0)
        self.assertEqual(self.statuses.count(), 2)
        self.assertRedirects(response, self.login_url)

    def test_auth_another_status_update_POST(self):
        self.client.force_login(self.user)
        self.client.post(self.status_create_url, {"name": "created1"})
        new_status = self.statuses.get(name="created1")
        self.status_update_url3 = reverse('status_update',
                                          kwargs={'pk': new_status.pk})
        self.assertEqual(self.statuses.filter(name="created1").count(), 1)
        self.client.logout()
        self.assertEqual(auth.get_user(self.client).is_authenticated, False)
        self.client.force_login(self.user2)
        response = self.client.post(self.status_update_url3,
                                    {"name": "updated2"})
        self.assertEqual(self.statuses.get(name="updated2").name, 'updated2')
        self.assertEqual(self.statuses.filter(name='created1').count(), 0)
        self.assertRedirects(response, self.statuses_url)

    def test_auth_user_status_delete_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.status_delete_url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_auth_user_status_delete_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_delete_url1)
        self.assertEqual(self.statuses.count(), 1)
        self.assertRedirects(response, self.statuses_url)

    def test_anonym_user_status_delete_POST(self):
        self.assertEqual(self.statuses.count(), 2)
        response = self.client.post(self.status_delete_url1)
        self.assertEqual(self.statuses.count(), 2)
        self.assertRedirects(response, self.login_url)

    def test_anonym_user_status_delete_GET(self):
        response = self.client.get(self.status_delete_url1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
