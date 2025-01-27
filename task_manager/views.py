from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from task_manager.users.forms import LoginUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        messages.success(self.request, _('You are logged in'))
        return reverse_lazy('index')


class LogoutUser(LogoutView):
    def get_success_url(self):
        messages.info(self.request, _('You are logged out'))
        return reverse_lazy('index')


def page_not_found_view(request, *args, **kwargs):
    return render(request, '404.html', status=404)
