from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView

from src.mextalki.models import Announcement, Like, Post
from src.mextalki.utils import get_post_by_uid, get_user_by_uid

UserModel = get_user_model()


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'forum/announcements/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_already_liked_post'] = self._get_user_like(
            self.request.user, self.object.post,
        )
        return context

    def _get_user_like(self, user: UserModel, announcement: Post) -> bool:
        return Like.objects.filter(user=user, post=announcement)


@csrf_protect
@require_http_methods(['POST'])
def like_post(request, user_uid_b64, post_id):
    user = get_user_by_uid(user_uid_b64)
    post = get_post_by_uid(post_id)
    if user and post:
        like = Like(post=post, user=user)
        like.save()
        return JsonResponse(
            {
                'username': user.username,
                'post_id': post_id,
                'like_id': like.pk,
                'likes_count': post.likes_count,
            }, safe=False,
        )

    return JsonResponse(
        {
            'issue': 'no user or post was found',
        }, safe=False,
    )
