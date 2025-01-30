from django.test import TestCase
from ..forms import UserCreateForm
from ..views import (
    UsersIndexView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView
)
from django.urls import reverse, resolve
from django.contrib import auth
from .mixins import UsersViewTestMixin, UserCreateFormTestMixin


class UsersUrlsTest(TestCase):
    def test_index_url(self):
        url = reverse('users')
        self.assertEqual(resolve(url).func.view_class, UsersIndexView)

    def test_create_url(self):
        url = reverse('user_create')
        self.assertEqual(resolve(url).func.view_class, UserCreateView)

    def test_update_url(self):
        url = reverse('user_update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserUpdateView)

    def test_delete_url(self):
        url = reverse('user_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserDeleteView)


class UserCreateFormTest(UserCreateFormTestMixin, TestCase):
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


class UsersViewTest(UsersViewTestMixin, TestCase):
    fixtures = ['users']

    def test_users_index_GET(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_user_create_GET(self):
        response = self.client.get(self.user_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_user_create_success_POST(self):
        response = self.client.post(self.user_create_url, {
            'first_name': 'Emma',
            'last_name': 'Watson',
            'username': 'Hermione',
            'password1': '<PASSWORD>',
            'password2': '<PASSWORD>'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.users.count(), 2)
        self.assertEqual(self.users.get(username="Hermione").first_name, 'Emma')

    def test_user_create_no_data_POST(self):
        response = self.client.post(self.user_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.users.count(), 2)

# update
    def test_anonymous_client_users_update_GET(self):
        response = self.client.get(self.user1_update_url)
        self.assertEqual(auth.get_user(self.client).is_authenticated, False)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_client_users_update_POST(self):
        response = self.client.post(self.user1_update_url, {
            'first_name': 'Max',
            'last_name': 'Payne',
            'username': 'max_payne',
            'password1': '<PASSWORD>',
            'password2': '<PASSWORD>'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 2)

    def test_auth_client_users_update_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.user_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_auth_client_users_update_success_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.user1_update_url, {
            'first_name': 'Max',
            'last_name': 'Payne',
            'username': 'max_payne',
            'password1': '<PASSWORD>',
            'password2': '<PASSWORD>'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.get(username="max_payne").last_name,
                         'Payne')

    def test_auth_client_users_update_no_data_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.user1_update_url, {})
        self.assertEqual(response.status_code, 200)

    def test_auth_client_users_update_exist_data_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.user1_update_url,
                                    kwargs=self.test_user2)
        self.assertEqual(response.status_code, 200)

# delete
    def test_anonymous_client_users_delete_GET(self):
        response = self.client.get(self.user_delete_url, {
            'pk': self.test_user.id,
        })
        self.assertEqual(response.status_code, 302)

    def test_anonymous_client_users_delete_POST(self):
        response = self.client.post(self.user_delete_url, {
            'pk': self.test_user.id,
        })
        self.assertEqual(self.users.count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_auth_client_users_delete_GET(self):
        self.client.force_login(self.test_user)
        response = self.client.get(self.user_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')

    def test_auth_client_users_delete_success_POST(self):
        self.client.force_login(self.test_user)
        self.assertEqual(auth.get_user(self.client).is_authenticated, True)
        response = self.client.post(self.user_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 1)
        self.assertEqual(auth.get_user(self.client).is_authenticated, False)

    def test_auth_client_users_delete_another_user_POST(self):
        self.client.force_login(self.test_user)
        self.assertEqual(auth.get_user(self.client).is_authenticated, True)
        response = self.client.post(self.user2_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 2)
        self.assertEqual(auth.get_user(self.client).is_authenticated, True)
