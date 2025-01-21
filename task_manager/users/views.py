from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from task_manager.users.forms import UserCreateForm
from task_manager.view_mixins import IndexViewMixin

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from . import forms


class UserPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request,
                           _("You can't edit other user's profile."))
            return redirect(reverse_lazy('users'))
        else:
            messages.error(self.request,
                           _("You are not authorized! Please log in."))
            return redirect(reverse_lazy('login'))


class UsersAbstractMixin:
    model = get_user_model()
    success_url = reverse_lazy('users')
    form_class = UserCreateForm


class UsersIndexView(UsersAbstractMixin, IndexViewMixin):
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(UsersAbstractMixin, CreateView):
    template_name = 'users/create.html'

    def get_success_url(self):
        messages.success(self.request,
                         _('User has been registered successfully.'))
        return reverse_lazy('login')


class UserUpdateView(UserPermissionMixin,
                     SuccessMessageMixin,
                     UpdateView):

    model = User
    form_class = forms.CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('User updated successfully')


class UserDeleteView(UserPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('User deleted successfully')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            messages.success(self.request, self.success_message)
        except ProtectedError:
            messages.error(self.request, _("User can't be deleted as long as they're involved in tasks")) # noqa
        return redirect(self.success_url)
