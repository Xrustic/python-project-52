from .models import Label
from django.urls import reverse_lazy
from task_manager.access_mixins import LoginRequireMixin
from .forms import LabelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect


class LabelAbstractMixin(LoginRequireMixin):
    model = Label
    login_url = "/login/"
    success_url = reverse_lazy('labels')
    form_class = LabelForm


class LabelIndexView(LabelAbstractMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(LabelAbstractMixin, CreateView):
    template_name = 'labels/create.html'

    def get_success_url(self):
        messages.success(self.request,
                         _('labels has been created successfully.'))
        return reverse_lazy('labels')


class LabelDeleteView(LoginRequireMixin, DeleteView):
    model = Label
    login_url = "/login/"
    template_name = 'labels/delete.html'

    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(
                self.request,
                _('Cannot delete labels because it is in use.'))
            return redirect('labels')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request,
                         _('labels has been deleted successfully.'))
        return reverse_lazy('labels')


class LabelUpdateView(LabelAbstractMixin, UpdateView):
    template_name = 'labels/update.html'

    def get_success_url(self):
        messages.success(self.request,
                         _('labels has been updated successfully.'))
        return reverse_lazy('labels')
