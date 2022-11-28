from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.mextalki.models import (
    Carousel,
    Faq,
    HomeCopyInfo,
    Lesson,
    MainCopy,
    Teacher,
    Testimonial,
)
from src.subscription.models import Subscription


class IndexView(TemplateView):
    template_name = 'index.html'
    forum_template_name = 'forum/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('default_forum_home')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(active=True)
        context['carousel_testimonials'] = Paginator(
            Testimonial.objects.filter(active=True),
            3,
        )
        context['carousel_items'] = Carousel.objects.filter(active=True).order_by('id')
        context['copy_sections'] = HomeCopyInfo.objects.filter(active=True)
        context['main_copy'] = MainCopy.objects.filter(active=True)
        context['faq'] = Faq.objects.filter(active=True).first()
        context['users'] = Subscription.objects.filter(active=True)
        context['teachers'] = Teacher.objects.filter(active=True)
        return context
