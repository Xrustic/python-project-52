from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from task_manager.view_mixins import IndexViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from task_manager.users.mixins import UserCreatorOnlyMixin


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


class UserUpdateView(UserCreatorOnlyMixin, UpdateView, LogoutView):
    model = get_user_model()
    form_class = UserUpdateForm
    login_url = '/login/'
    success_url = reverse_lazy('users')
    template_name = 'users/update.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        if pk != self.request.user.id:
            messages.error(request,
                           _('You do not have permission to'
                             ' change another user.'))
            return HttpResponseRedirect(reverse('users'))
        else:
            form = UserCreateForm(instance=user)
            return render(request, 'users/update.html', {'form': form})

    def get_success_url(self):
        messages.success(self.request,
                         _('User has been updated successfully.'))
        return reverse_lazy('users')


class UserDeleteView(LoginRequiredMixin, DeleteView):
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
