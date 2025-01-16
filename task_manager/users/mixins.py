from task_manager.access_mixins import LimitedPermissionsMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class UserCreatorOnlyMixin(LimitedPermissionsMixin):
    redirect_url = reverse_lazy('users')
    permission_denied_message = _("""You do not have permission to edit
                                  another user""")
    have_permission = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.id == kwargs.get('pk'):
            self.have_permission = True
        return super().dispatch(request, *args, **kwargs)
