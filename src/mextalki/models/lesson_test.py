from types import MappingProxyType

from django.db import models

from src.mextalki.models.base_model import TimeStampMixin


class Question(TimeStampMixin):
    test = models.ForeignKey(
        'mextalki.LessonTest',
        on_delete=models.PROTECT,
        related_name='questions',
        null=True,
        blank=True,
        default=None,
    )
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Answer(TimeStampMixin):
    question = models.ForeignKey(
        'mextalki.Question',
        on_delete=models.PROTECT,
        related_name='answers',
        null=True,
        blank=True,
        default=None,
    )
    answer = models.CharField(max_length=255)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class LessonTest(TimeStampMixin):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    instructions = models.TextField(blank=True, null=True)

    lesson = models.ForeignKey(
        'mextalki.Lesson',
        on_delete=models.PROTECT,
        related_name='tests',
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        verbose_name_plural = 'Lessons - Tests'

    def __str__(self):
        return self.title


class TestScore(TimeStampMixin):
    EXP_POINTS = MappingProxyType({
        0: 10,
        1: 7,
        2: 2,
    })

    test = models.ForeignKey(
        'mextalki.LessonTest',
        on_delete=models.PROTECT,
        related_name='scores',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='scores',
    )
    active = models.BooleanField(
        default=True,
    )
    attempt_counter = models.PositiveIntegerField(
        default=0,
    )
    full_well_answered = models.BooleanField(
        default=False,
    )
    correct_answered = models.PositiveIntegerField(
        default=0,
    )
    exp_points = models.FloatField(
        default=0,
    )

    @property
    def possible_max_score(self):
        if self.attempt_counter < 3:
            return self.EXP_POINTS[self.attempt_counter]
        else:
            return self.EXP_POINTS[2]

    def __str__(self) -> str:
        return '{} by {}'.format(self.test, self.user)
