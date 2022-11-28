import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView

from src.mextalki.forms import LessonTestForm
from src.mextalki.logger import logger
from src.mextalki.models import (
    Course,
    EventType,
    Lesson,
    LessonTest,
    ScheduledEvent,
    Teacher,
    TestScore,
)
from src.mextalki.utils import get_event_type_by_uid, get_user_by_uid
from src.mextalki.utils.schedule_event import create_scheduled_event
from src.users.models import User


class LessonView(FormView):
    form_class = LessonTestForm
    lesson: Lesson = None
    course: Course = None
    score: TestScore = None
    test: LessonTest = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.course = get_object_or_404(Course, slug=kwargs.get('course'))
        self.lesson = get_object_or_404(Lesson, slug=kwargs.get('lesson'))
        self.test = self._get_test()
        self.score = self._get_score()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['test'] = self.test
        return kwargs

    def get_template_names(self):
        template = 'lessons/no_access.html'
        if self._user_has_access_to_lesson():
            if self.lesson.type == 'LESSON':
                template = 'lessons/lesson.html'
            elif self.lesson.type == 'MODULE':
                template = 'lessons/module.html'
        return [template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.lesson
        context['course_slug'] = self.course.slug
        context['test'] = self.test
        context['score'] = self.score
        context['disable_lp_transcription_button'] = self._disable_lp_transcription_button()
        context['disable_lp_show_answers_button'] = self._disable_lp_show_answers_button()
        context['disable_sp_exercises_button'] = self._disable_sp_exercises_button()
        context['disable_sp_audios_button'] = self._disable_sp_audios_button()
        context['next_lesson'] = self._get_next_lesson()
        return context

    def get_success_url(self, **kwargs):
        return reverse(
            'lesson_detail',
            kwargs={
                'course': self.course.slug,
                'lesson': self.lesson.slug,
            },
        )

    def form_valid(self, form):
        self.score.full_well_answered = True
        self.score.correct_answered = form.correct_answered
        self.score.exp_points = self.score.possible_max_score
        self.score.attempt_counter += 1
        self.score.test = self.test
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

    def _user_has_access_to_lesson(self):
        if self.lesson.free:
            return True
        user: User = self.request.user
        if user.is_authenticated:
            return user.has_access_to_course(self.course)
        return False

    def _get_test(self):
        return self.lesson.main_test

    def _get_score(self):
        user = self.request.user
        if not user.is_authenticated:
            return None
        if not self.test:
            return None
        try:
            return TestScore.objects.get(user=user, test=self.lesson.main_test)
        except TestScore.DoesNotExist:
            return TestScore(user=user, test=self.lesson.main_test)

    def _disable_lp_transcription_button(self):
        disable_button = True
        try:
            for audio in self.lesson.listening_practice.get_audios():
                if audio.transcription:
                    disable_button = False
        except ObjectDoesNotExist as error:
            logger.error(error)
        return disable_button

    def _disable_lp_show_answers_button(self):
        disable_button = True
        try:
            for audio in self.lesson.listening_practice.get_audios():
                if audio.answer:
                    disable_button = False
        except ObjectDoesNotExist as error:
            logger.error(error)
        return disable_button

    def _disable_sp_exercises_button(self):
        try:
            return len(self.lesson.speaking_practice.get_resources()) == 0
        except ObjectDoesNotExist as error:
            logger.error(error)
            return True

    def _disable_sp_audios_button(self):
        try:
            return len(self.lesson.speaking_practice.get_audios()) == 0
        except ObjectDoesNotExist as error:
            logger.error(error)
            return True

    def _get_next_lesson(self):
        lessons = []
        next_lesson = None
        for level in self.course.get_levels():
            for module in level.get_modules():
                for lesson in module.get_lessons():
                    lessons.append(lesson)
        for key, lesson in enumerate(lessons):
            try:
                if lesson == self.lesson:
                    next_lesson = lessons[key + 1]
            except IndexError:
                next_lesson = None
        return next_lesson


class ScheduleLessonView(TemplateView):
    template_name = 'lessons/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(active=True)
        return context


@csrf_protect
@require_http_methods(['POST'])
def schedule_lesson_view(request, user_uid_b64, event_type_uid_b64):
    user: User = get_user_by_uid(user_uid_b64)
    event_type: EventType = get_event_type_by_uid(event_type_uid_b64)
    if user and event_type:
        payload = _get_request_payload(request)
        create_scheduled_event(
            user=user,
            event_type=event_type,
            teacher=event_type.teacher,
            provider=ScheduledEvent.CALENDLY,
            provider_event_id=payload['event_id'],
            provider_invite_id=payload['invitee_id'],
        )
        status_code = HttpResponse.status_code
        _set_message_success(
            request,
            'Your lesson has been correctly scheduled.',
        )
    else:
        status_code = HttpResponseBadRequest.status_code
        _set_message_error(
            request,
            'Sorry your payment was not processed correctly, try again.',
        )
    response = {
        'status': status_code,
    }
    return JsonResponse(response, status=status_code)


def _get_request_payload(request):
    return json.loads(request.body.decode('utf-8'))


def _set_message_success(request, message):
    messages.success(request, message)


def _set_message_error(request, message):
    messages.error(request, message)
