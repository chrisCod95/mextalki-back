from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View


class LogoutRequiredMixin(View):

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(*args, **kwargs)
