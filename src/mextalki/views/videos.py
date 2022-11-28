import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from taggit.models import Tag, TaggedItem

from src.mextalki.models import CommonVideoScore, Video
from src.mextalki.utils import (
    get_user_by_uid,
    get_video_by_uid,
    get_video_score_by_user,
)


class VideosListView(ListView):
    paginate_by: int = 12
    model: Video = Video
    template_name = 'video/video_list.html'

    def get_context_data(self, **kwargs):
        context = super(VideosListView, self).get_context_data(**kwargs)
        context['tags'] = self.get_unique_tags()
        context['selected_tag'] = self.request.GET.get('tag')
        return context

    def get_queryset(self):
        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            return Video.objects.filter(tags__slug=tag_filter, active=True)
        return Video.objects.filter(active=True)

    def get_unique_tags(self):
        videos_queryset = self.model.objects.filter(active=True)
        my_class_ct = ContentType.objects.get_for_model(self.model)
        unique_tag_ids = set(
            TaggedItem.objects.filter(
                content_type=my_class_ct,
                object_id__in=videos_queryset,
            ).values_list(
                'tag',
                flat=True,
            ),
        )
        return Tag.objects.filter(pk__in=unique_tag_ids).order_by('name')


class VideoDetailView(DetailView):
    model: Video = Video
    template_name = 'video/video_detail.html'
    video_score: CommonVideoScore = None

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            self.video_score = self._get_video_score(self.object)
            context['video_score'] = self.video_score
        return context

    def _get_video_score(self, video: Video):
        try:
            return CommonVideoScore.objects.get(
                user=self.request.user,
                video=video,
            )
        except CommonVideoScore.DoesNotExist:
            return CommonVideoScore(
                user=self.request.user,
                video=video,
            )


@csrf_protect
@require_http_methods(['POST'])
def redeem_points_to_common_video_score(request, user_uid_b64, video_id):
    user = get_user_by_uid(user_uid_b64)
    video = get_video_by_uid(video_id)
    if user and video:
        video_score = get_video_score_by_user(video, user)
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
        'redirect_url': reverse_lazy('videos_list'),
    }
    return JsonResponse(response, status=status_code)


def get_request_payload(request):
    return json.loads(request.body.decode('utf-8'))
