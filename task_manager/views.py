from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from task_manager.users.forms import LoginUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
# import rollbar
# import os
#
# # Инициализация Rollbar
# rollbar.init(
#     access_token=os.getenv("ROLLBAR_ACCESS_TOKEN"),
#     environment='production',
# )
#
# # Пример обработки ошибки и отправки в Rollbar
# try:
#     result = 1 / 0  # Искусственная ошибка
# except ZeroDivisionError as e:
#     rollbar.report_exc_info()  # Сообщить об ошибке
#     print("Ошибка отправлена в Rollbar!")
#
# # Пример отправки произвольного сообщения в Rollbar
# rollbar.report_message('Тестовое сообщение', level='info')


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
