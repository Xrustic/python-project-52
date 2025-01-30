from django.test import TestCase
from task_manager.tasks.forms import TaskForm
from django.urls import reverse, resolve
from task_manager.tasks.views import (
    TaskIndexView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView
)
from django.contrib import auth
from .mixins import (
    TaskViewsTestMixin,
    TaskCreationFormTestMixin
)


class TasksUrlTest(TestCase):

    def test_task_index_url(self):
        url = reverse('tasks')
        self.assertEqual(resolve(url).func.view_class, TaskIndexView)

    def test_task_create_url(self):
        url = reverse('task_create')
        self.assertEqual(resolve(url).func.view_class, TaskCreateView)

    def test_task_update_url(self):
        url = reverse('task_update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskUpdateView)

    def test_task_detail_url(self):
        url = reverse('task_detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskDetailView)

    def test_task_delete_url(self):
        url = reverse('task_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskDeleteView)


class TaskCreationFormTest(TaskCreationFormTestMixin, TestCase):
    fixtures = ['users', 'statuses']

    def test_creation_form_with_valid_data(self):
        form = TaskForm(self.form_data.get('Task1'))
        self.assertTrue(form.is_valid())

    def test_creation_form_with_invalid_data(self):
        form = TaskForm(self.form_data.get('Task2'))
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['name'])
        self.assertTrue(form.errors['status'])
        self.assertEqual(len(form.errors), 2)

    def test_creation_form_with_no_data(self):
        form = TaskForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class TaskViewsTest(TaskViewsTestMixin, TestCase):
    fixtures = ['users', 'labels', 'statuses', 'tasks']

    def test_tasks_filter_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.context['tasks'].count(), 3)
        response = self.client.get(self.tasks_url, {'labels': 1})
        self.assertEqual(response.context['tasks'].count(), 1)
        response = self.client.get(self.tasks_url, {'author': 'on'})
        self.assertEqual(response.context['tasks'].count(), 2)
        response = self.client.get(self.tasks_url,
                                   {'author': 'on', 'labels': 1})
        self.assertEqual(response.context['tasks'].count(), 1)
        response = self.client.get(self.tasks_url, {'status': 1})
        self.assertEqual(response.context['tasks'].count(), 2)

    def test_anonym_user_tasks_index(self):
        response = self.client.get(self.tasks_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_tasks_index(self):
        self.client.force_login(self.user)
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_auth_user_task_create_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_anonym_user_task_create_GET(self):
        response = self.client.get(self.task_create_url)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_task_create_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(
            self.task_create_url, {
                "name": "new_task",
                "status": 1
            }
        )
        self.assertEqual(self.tasks.get(name='new_task').name, 'new_task')
        self.assertEqual(self.tasks.count(), 4)
        self.assertRedirects(response, self.tasks_url)

    def test_auth_user_task_create_no_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(self.task_create_url)
        self.assertEqual(response.status_code, 200)

    def test_auth_user_task_create_exist_data_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(
            self.task_create_url, {
                "name": "Test Task1",
                "status": 1
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_anonym_user_task_create_POST(self):
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(
            self.task_create_url, {
                "name": "new_status1",
                "status": 1
            }
        )
        self.assertEqual(self.tasks.count(), 3)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_task_update_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_update_url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')

    def test_anonym_user_task_update_GET(self):
        response = self.client.get(self.task_update_url1)
        self.assertRedirects(response, self.login_url)

    def test_auth_user_task_update_success_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(
            self.task_update_url1, {
                "name": "updated1",
                "status": 1
            }
        )
        self.assertEqual(self.tasks.count(), 3)
        self.assertEqual(self.tasks.get(name="updated1").name, "updated1")
        self.assertRedirects(response, self.tasks_url)

    def test_auth_user_task_update_fail_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(self.task_update_url1,
                                    {"name": "", "status": 1})
        self.assertEqual(
            self.tasks.get(name="Test Task1").name,
            "Test Task1"
        )
        self.assertEqual(response.status_code, 200)

    def test_anonym_user_task_update_POST(self):
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(
            self.task_update_url1, {
                "name": "updated1",
                "status": 1
            }
        )
        self.assertEqual(self.tasks.filter(name="updated1").count(), 0)
        self.assertEqual(self.tasks.count(), 3)
        self.assertRedirects(response, self.login_url)

    def test_auth_another_task_update_POST(self):
        self.client.force_login(self.user)
        self.client.post(self.task_create_url,
                         {"name": "created1", "status": 1})
        new_task = self.tasks.get(name="created1")
        self.task_update_url3 = reverse(
            'task_update',
            kwargs={'pk': new_task.pk}
        )
        self.assertEqual(self.tasks.filter(name="created1").count(), 1)
        self.client.logout()
        self.assertEqual(auth.get_user(self.client).is_authenticated, False)
        self.client.force_login(self.user2)
        response = self.client.post(
            self.task_update_url3, {
                "name": "updated2",
                "status": 1
            }
        )
        self.assertEqual(self.tasks.get(name="updated2").name, 'updated2')
        self.assertEqual(self.tasks.filter(name='created1').count(), 0)
        self.assertRedirects(response, self.tasks_url)

    def test_auth_user_task_delete_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_delete_url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_auth_user_task_delete_POST(self):
        self.client.force_login(self.user)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(self.task_delete_url1)
        self.assertEqual(self.tasks.count(), 2)
        self.assertRedirects(response, self.tasks_url)

    def test_auth_another_user_task_delete_POST(self):
        self.client.force_login(self.user2)
        self.assertEqual(self.tasks.count(), 3)
        response = self.client.post(self.task_delete_url1)
        self.assertEqual(self.tasks.count(), 3)
        self.assertRedirects(response, self.tasks_url)

    def test_auth_user_task_detail_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.task_view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')

    def test_anonym_user_task_detail_GET(self):
        response = self.client.get(self.task_view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
