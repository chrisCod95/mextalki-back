
from django.views.generic.detail import DetailView

from src.mextalki.models import Course
from src.users.models import User


class CoursesView(DetailView):
    model = Course
    template_name = 'courses/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_access_to_course'] = self.user_has_access_to_course()
        return context

    def user_has_access_to_course(self) -> bool:
        user: User = self.request.user
        if user.is_authenticated:
            return user.has_access_to_course(self.object)
        return False
