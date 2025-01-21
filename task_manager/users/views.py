from django.contrib.auth import get_user_model
# from django.shortcuts import render
from django.urls import reverse_lazy
# , reverse)
# from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from task_manager.users.forms import UserCreateForm
# , UserUpdateForm)
from task_manager.view_mixins import IndexViewMixin
# , UpdateViewMixin)
from task_manager.access_mixins import LoginRequireMixin

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
# class UserUpdateView(LoginRequireMixin, UsersAbstractMixin,
# UpdateViewMixin, UpdateView):
#     model = get_user_model()
#     form_class = UserUpdateForm
#     login_url = '/login/'
#     success_url = reverse_lazy('users')
#     template_name = 'users/update.html'
#
#     def get(self, request, pk):
#         user = User.objects.get(id=pk)
#         if pk != self.request.user.id:
#             messages.error(request,
#                            _('You do not have permission to'
#                              ' change another user.'))
#             return HttpResponseRedirect(reverse('users'))
#         else:
#             form = UserUpdateForm(instance=user)
#             return render(request, 'users/update.html', {'form': form})
#
#     def get_success_url(self):
#         messages.success(self.request,
#                          _('User has been updated successfully.'))
#         return reverse_lazy('users')


class UserDeleteView(LoginRequireMixin, DeleteView):
    model = get_user_model()
    login_url = '/login/'
    template_name = 'users/delete.html'

    def post(self, request, pk):
        user = self.get_object()

        if user.tasks_author.exists() or user.tasks_executor.exists():
            messages.error(request, _(
                'Cannot delete user. User is associated with tasks.'))
        elif pk != self.request.user.id:
            messages.error(request, _(
                'You do not have permission to delete another user.'))
        else:
            user.delete()
            messages.success(request, _(
                'User has been deleted successfully.'))
            return redirect('index')

        return redirect('users')

    def get_success_url(self):
        messages.success(self.request,
                         _('User has been deleted successfully.'))
        return reverse_lazy('index')
