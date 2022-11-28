from django.views.generic import DetailView, ListView

from src.mextalki.models import BlogPost


class BlogListView(ListView):
    paginate_by: int = 12
    model = BlogPost
    template_name = 'blog/list.html'


class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
