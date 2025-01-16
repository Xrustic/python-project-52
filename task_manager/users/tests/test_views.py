from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib import auth
import os


@override_settings(
    SECRET_KEY='fake-key',
    FIXTURE_DIRS=[os.path.join(os.path.dirname(__file__), 'fixtures')]
)
class UsersViewTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.client = Client()
        self.users_url = reverse('users')
        self.user_create_url = reverse('user_create')
        self.users = auth.get_user_model().objects
        self.test_user = self.users.get(username='max_payne')
        self.test_user2 = self.users.get(username='Hermione')
        self.user_update_url = reverse('users')
        self.user1_update_url = reverse('user_update', kwargs={'pk': self.test_user.id})
        self.user2_update_url = reverse('user_update', kwargs={'pk': self.test_user2.id})
        self.user_delete_url = reverse('user_delete', kwargs={'pk': self.test_user.id})
        self.user2_delete_url = reverse('user_delete', kwargs={'pk': self.test_user2.id})

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
        self.assertEqual(self.users.get(username="max_payne").last_name, 'Smith')

    def test_auth_client_users_update_no_data_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.user1_update_url, {})
        self.assertEqual(response.status_code, 302)

    def test_auth_client_users_update_exist_data_POST(self):
        self.client.force_login(self.test_user)
        response = self.client.post(self.user1_update_url, kwargs=self.test_user2)
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
