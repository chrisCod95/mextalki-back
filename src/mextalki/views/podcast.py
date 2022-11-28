import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, ListView
from taggit.models import Tag, TaggedItem

from src.mextalki.forms import PodcastTestForm
from src.mextalki.models import Podcast, PodcastTest, PodcastTestScore, VideoScore
from src.mextalki.utils import (
    get_podcast_by_uid,
    get_podcast_video_score_by_user,
    get_user_by_uid,
)


class PodcastListView(ListView):
    paginate_by = 12
    model = Podcast
    template_name = 'podcast/list.html'

    def get_context_data(self, **kwargs):
        context = super(PodcastListView, self).get_context_data(**kwargs)
        context['tags'] = self.get_unique_tags()
        context['selected_tag'] = self.request.GET.get('tag')
        return context

    def get_queryset(self):
        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            return Podcast.objects.filter(tags__slug=tag_filter, active=True)
        return Podcast.objects.filter(active=True)

    def get_unique_tags(self):
        podcast_queryset = self.model.objects.filter(active=True)
        my_class_ct = ContentType.objects.get_for_model(self.model)
        unique_tag_ids = set(
            TaggedItem.objects.filter(
                content_type=my_class_ct,
                object_id__in=podcast_queryset,
            ).values_list(
                'tag',
                flat=True,
            ),
        )
        return Tag.objects.filter(pk__in=unique_tag_ids).order_by('name')


class PodcastView(FormView):
    template_name = 'podcast/index.html'
    form_class = PodcastTestForm
    test: PodcastTest = None
    score: PodcastTestScore = None
    podcast: Podcast = None
    video_score = VideoScore = None

    def setup(self, request, *args, **kwargs):
        super(PodcastView, self).setup(request, *args, **kwargs)
        self.podcast = get_object_or_404(
            Podcast,
            slug=kwargs['slug'],
        )
        if request.user.is_authenticated:
            self.test = self._get_test(self.podcast)
            self.score = self._get_score(self.test)
            self.video_score = self._get_video_score(self.podcast)

    def get_form_kwargs(self):
        kwargs = super(PodcastView, self).get_form_kwargs()
        kwargs['test'] = self.test
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PodcastView, self).get_context_data(**kwargs)
        context['object'] = self.podcast
        context['test'] = self.test
        context['score'] = self.score
        context['video_score'] = self.video_score
        return context

    def get_success_url(self, **kwargs):
        return reverse(
            'podcast_detail',
            kwargs={
                'slug': self.podcast.slug,
            },
        )

    def form_valid(self, form):
        self.score.full_well_answered = True
        self.score.correct_answered = form.correct_answered
        self.score.exp_points = self.score.possible_max_score
        self.score.attempt_counter += 1
        self.score.save()
        self.request.user.leadership_board_score_sum(
            self.score.exp_points, category='tests',
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        self.score.correct_answered = form.correct_answered
        self.score.attempt_counter += 1
        self.score.save()
        return super().form_invalid(form)

    def _get_test(self, podcast: Podcast):
        return podcast.tests.first()

    def _get_score(self, test: PodcastTest):
        if not test:
            return None
        try:
            return PodcastTestScore.objects.get(
                user=self.request.user,
                test=test,
            )
        except PodcastTestScore.DoesNotExist:
            return PodcastTestScore(
                user=self.request.user,
                test=test,
            )

    def _get_video_score(self, podcast: Podcast):
        try:
            return VideoScore.objects.get(
                user=self.request.user,
                podcast=podcast,
            )
        except VideoScore.DoesNotExist:
            return VideoScore(
                user=self.request.user,
                podcast=podcast,
            )


@csrf_protect
@require_http_methods(['POST'])
def redeem_points_to_video_score(request, user_uid_b64, podcast_id):
    user = get_user_by_uid(user_uid_b64)
    podcast = get_podcast_by_uid(podcast_id)
    if user and podcast:
        video_score = get_podcast_video_score_by_user(podcast, user)
        request_payload = get_request_payload(request)
        achieved_points = request_payload.get('achieved_points', 0)
        user.leadership_board_score_sum(achieved_points, category='videos')
        video_score.exp_points = achieved_points
        video_score.user_already_get_points = True
        video_score.save()
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    response = {
        'status': status_code,
        'redirect_url': reverse_lazy('podcast'),
    }
    return JsonResponse(response, status=status_code)


def get_request_payload(request):
    return json.loads(request.body.decode('utf-8'))
