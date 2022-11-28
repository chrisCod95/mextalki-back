from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView

from src.mextalki.forms import CommentForm
from src.mextalki.models import Challenge, Comment, Like
from src.mextalki.utils import get_comment_by_id, get_user_by_uid

UserModel = get_user_model()


class ChallengeDetailView(FormView):
    template_name = 'forum/challenges/detail.html'
    form_class = CommentForm
    challenge: Challenge = None
    user_answer = Comment = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.challenge = get_object_or_404(Challenge, slug=kwargs['slug'])
        self.user_answer = self._get_user_answer()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenge'] = self.challenge
        context['user_answer'] = self.user_answer
        context['user_answered_correctly'] = self._user_answered_correctly()
        context['comments'] = Comment.objects.filter(
            active=True,
            post=self.challenge.post,
        ).exclude(user=self.request.user)
        return context

    def form_valid(self, form):
        content = form.cleaned_data['content']
        user = self.request.user
        post = self.challenge.post
        Comment(user=user, post=post, content=content).save()
        return super().form_valid(form)

    def _get_user_answer(self):
        try:
            return Comment.objects.get(user=self.request.user, post=self.challenge.post)
        except Comment.DoesNotExist:
            return None

    def _user_answered_correctly(self):
        try:
            return Comment.objects.get(user=self.request.user, post=self.challenge.post, is_challenge_correct_answer=True)
        except Comment.DoesNotExist:
            return False

    def get_success_url(self, **kwargs):
        return reverse(
            'challenge_detail',
            kwargs={
                'slug': self.challenge.slug,
            },
        )


@csrf_protect
@require_http_methods(['POST'])
def challenge_correct_answer(request, user_uid_b64, comment_id):
    points_to_add = 20
    user = get_user_by_uid(user_uid_b64)
    comment = get_comment_by_id(comment_id)
    if user and comment:
        comment.is_challenge_correct_answer = True
        comment.save()
        request.user.leadership_board_score_sum(
            points_to_add, category='challenges',
        )
        return redirect(
            reverse(
                'challenge_detail',
                kwargs={
                    'slug': comment.post.challenge.slug,
                },
            ),
        )

    return redirect(
        reverse(
            'challenge_detail',
            kwargs={
                'slug': comment.post.challenge.slug,
            },
        ),
    )
