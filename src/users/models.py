from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from src.mextalki.logger import logger
from src.mextalki.models import (
    Comment,
    Course,
    LeadershipScore,
    Plan,
    UserAvailableLessonTime,
    UserExperiencePoint,
    UserReferralCredits,
)
from src.mextalki.models.utils import upload_to_v2
from src.subscription.models import Subscription
from src.users.get_mask import MAX_EXP_POINTS, get_mask
from src.users.manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        _(
            'email address',
        ),
        unique=True,
    )
    bio = models.TextField(
        max_length=500,  # noqa: WPS432
        blank=True,
    )
    location = models.CharField(
        max_length=30,  # noqa: WPS432
        blank=True,
    )
    birth_day = models.DateField(
        null=True,
        blank=True,
    )
    verified = models.BooleanField(
        default=False,
        help_text='Designates whether this user should be treated as verified with email.',
    )

    profile_picture = models.ImageField(
        upload_to=upload_to_v2,
        blank=True,
        null=True,
        default=None,
    )

    slug = models.SlugField(
        blank=True,
        null=True,
    )

    file_path = 'users/profile_pictures'

    USERNAME_FIELD = 'email'  # noqa: WPS115
    REQUIRED_FIELDS = ['username']  # noqa: WPS115

    objects = CustomUserManager()  # noqa: WPS110

    is_teacher = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    @property
    def teacher_profile(self):
        return self.teacher_profile

    @property
    def payment_courses(self):
        course_id_list: list = self.plan_payments.values_list('plan__course__id', flat=True)
        return Course.objects.filter(pk__in=course_id_list)

    @property
    def subscription_courses(self):
        if self.has_access_to_courses:
            return Course.objects.filter(active=True)
        return Course.objects.none()

    @property
    def courses(self):
        return self.payment_courses | self.subscription_courses

    @property
    def last_subscription(self):
        return self.subscriptions.order_by('-created_at').first()

    @property
    def has_active_subscription(self) -> bool:
        subscription: Subscription = self.last_subscription
        if subscription:
            if subscription.status == subscription.CREATED:
                return True
            if subscription.status in (subscription.CANCELLED or subscription.EXPIRED):
                return timezone.now() <= subscription.next_billing_time
            return subscription.active
        return False

    @admin.display(boolean=True)
    def has_active_subscription_for_admin(self) -> bool:
        if self.has_active_subscription:
            return True
        return False

    @property
    def has_access_to_courses(self) -> bool:
        if self.has_active_subscription:
            return self.last_subscription.subscription_type.has_access_to_courses
        return False

    @property
    def total_lesson_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.lesson_time + related_available_time.purchased_lesson_time

    @property
    def total_practice_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.practice_time + related_available_time.purchased_practice_time

    @property
    def total_available_conversation_club_slots(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.conversation_club_slots + related_available_time.purchased_conversation_club_slots

    @property
    def available_lesson_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.lesson_time

    @property
    def available_practice_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.practice_time

    @property
    def purchased_lesson_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.purchased_lesson_time

    @property
    def purchased_practice_time(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.purchased_practice_time

    @property
    def purchased_conversation_club_slots(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.purchased_conversation_club_slots

    @property
    def available_conversation_club_slots(self) -> int:
        related_available_time = self._get_user_related_available_time()
        return related_available_time.conversation_club_slots

    @property
    def scheduled_event_exp_points(self) -> int:
        try:
            return self.user_experience_points.scheduled_event_exp_points
        except ObjectDoesNotExist:
            return 0

    @property
    def referral_credits(self):
        try:
            return self.user_credits.credits
        except ObjectDoesNotExist:
            return 0

    @property
    def referred_users(self):
        return self.referrals.count()

    def has_access_to_course(self, course: Course):
        return course in self.courses

    def set_available_lesson_time(self, time):
        related_available_time = self._get_user_related_available_time()
        related_available_time.lesson_time = time
        related_available_time.save()

    def set_purchased_lesson_time(self, time):
        related_available_time = self._get_user_related_available_time()
        related_available_time.purchased_lesson_time = time
        related_available_time.save()

    def set_available_practice_time(self, time):
        related_available_time = self._get_user_related_available_time()
        related_available_time.practice_time = time
        related_available_time.save()

    def set_purchased_practice_time(self, time):
        related_available_time = self._get_user_related_available_time()
        related_available_time.purchased_practice_time = time
        related_available_time.save()

    def set_conversation_club_slots(self, slots):
        related_available_time = self._get_user_related_available_time()
        related_available_time.conversation_club_slots = slots
        related_available_time.save()

    def set_purchased_conversation_club_slots(self, slots):
        related_available_time = self._get_user_related_available_time()
        related_available_time.purchased_conversation_club_slots = slots
        related_available_time.save()

    def set_scheduled_event_exp_points(self, points: int):
        related_experience_points = self._get_user_related_experience_points()
        related_experience_points.scheduled_event_exp_points = points
        related_experience_points.save()

    def set_referral_credits(self, credits: int):
        related_credits = self._get_related_referral_credits()
        related_credits.credits = credits
        related_credits.save()

    def add_available_lesson_time(self, time):
        self.set_available_lesson_time(self.available_lesson_time + time)

    def remove_available_lesson_time(self, time):
        self.set_available_lesson_time(self.available_lesson_time - time)

    def add_purchased_lesson_time(self, time):
        self.set_purchased_lesson_time(self.purchased_lesson_time + time)

    def remove_purchased_lesson_time(self, time):
        self.set_purchased_lesson_time(self.purchased_lesson_time - time)

    def add_available_practice_time(self, time):
        self.set_available_practice_time(self.available_practice_time + time)

    def remove_available_practice_time(self, time):
        self.set_available_practice_time(self.available_practice_time - time)

    def add_purchased_practice_time(self, time):
        self.set_purchased_practice_time(self.purchased_practice_time + time)

    def remove_purchased_practice_time(self, time):
        self.set_purchased_practice_time(self.purchased_practice_time - time)

    def add_conversation_club_slots(self, slots):
        self.set_conversation_club_slots(self.available_conversation_club_slots + slots)

    def remove_conversation_club_slots(self, slots):
        self.set_conversation_club_slots(self.available_conversation_club_slots - slots)

    def add_purchased_conversation_club_slots(self, slots):
        self.set_purchased_conversation_club_slots(
            self.purchased_conversation_club_slots + slots,
        )

    def remove_purchased_conversation_club_slots(self, slots):
        self.set_purchased_conversation_club_slots(
            self.purchased_conversation_club_slots - slots,
        )

    def add_scheduled_event_exp_points(self, points):
        self.set_scheduled_event_exp_points(self.scheduled_event_exp_points + points)

    def remove_scheduled_event_exp_points(self, points):
        self.set_scheduled_event_exp_points(self.scheduled_event_exp_points - points)

    def add_referral_credits(self, credits: int):
        self.set_referral_credits(self.referral_credits + credits)

    def remove_referral_credits(self, credits: int):
        self.set_referral_credits(self.referral_credits - credits)

    def leadership_board_score_sum(self, points_to_add, category: str):
        related_leadership_score = self._get_related_leadership_board_score()
        if category == 'lesson_time':
            related_leadership_score.lesson_time_exp_points += points_to_add
        elif category == 'tests':
            related_leadership_score.tests_exp_points += points_to_add
        elif category == 'videos':
            related_leadership_score.videos_exp_points += points_to_add
        elif category == 'challenges':
            related_leadership_score.challenges_exp_points += points_to_add
        related_leadership_score.exp_points += points_to_add
        related_leadership_score.save()

    def leadership_board_score_subtract(self, points_to_subtract, category: str):
        related_leadership_score = self._get_related_leadership_board_score()
        if category == 'lesson_time':
            related_leadership_score.lesson_time_exp_points -= points_to_subtract
        elif category == 'tests':
            related_leadership_score.tests_exp_points -= points_to_subtract
        elif category == 'videos':
            related_leadership_score.videos_exp_points -= points_to_subtract
        related_leadership_score.exp_points -= points_to_subtract
        related_leadership_score.save()

    @property
    def referral_code(self):
        return urlsafe_base64_encode(force_bytes(self.username))

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def uid(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return static('default_profile.png')

    @property
    def mask_name(self):
        return get_mask(self.exp_points).get('name')

    @property
    def mask(self):
        image = get_mask(self.exp_points).get('image')
        return static(image)

    @property
    def exp_points(self) -> int:
        exp_points: int = self.lesson_exp_points + self.scheduled_event_exp_points + \
            self.video_exp_points + self.common_video_exp_points + self.challenges_exp_points
        if exp_points > MAX_EXP_POINTS:
            return MAX_EXP_POINTS
        return exp_points

    @property
    def challenges_exp_points(self):
        points_per_correct_answer = 20
        correct_answers = Comment.objects.filter(
            user=self, is_challenge_correct_answer=True,
        ).count()
        if correct_answers:
            return points_per_correct_answer * correct_answers
        return 0

    @property
    def common_video_exp_points(self):
        aggregate = self.common_video_scores.aggregate(models.Sum('exp_points'))[
            'exp_points__sum'
        ] or 0
        return aggregate

    @property
    def video_exp_points(self):
        aggregate = self.video_scores.aggregate(models.Sum('exp_points'))[
            'exp_points__sum'
        ] or 0
        return aggregate

    @property
    def lesson_exp_points(self):
        aggregate = self.scores.aggregate(models.Sum('exp_points'))[
            'exp_points__sum'
        ] or 0
        return aggregate

    @property
    def exp_points_percentage(self):
        exp_points = self.exp_points
        if exp_points <= 100:
            return exp_points * 100 / 100
        elif 100 < exp_points <= 200:
            return (exp_points - 100) * 100 / 100
        elif 200 < exp_points <= 400:
            return (exp_points - 200) * 100 / 200
        elif 400 < exp_points <= 800:
            return (exp_points - 400) * 100 / 400
        elif 800 < exp_points <= MAX_EXP_POINTS:
            return (exp_points - 800) * 100 / 400
        return 100

    @property
    def max_point_scale(self):
        exp_points = self.exp_points
        if exp_points <= 100:
            return 100
        elif 100 < exp_points <= 200:
            return 200
        elif 200 < exp_points <= 400:
            return 400
        elif 400 < exp_points <= 800:
            return 800
        elif 800 < exp_points <= MAX_EXP_POINTS:
            return MAX_EXP_POINTS
        return MAX_EXP_POINTS

    def _get_user_related_available_time(self) -> UserAvailableLessonTime:
        try:
            return self.user_available_lesson_time
        except ObjectDoesNotExist as error:
            logger.error(error)
            available_lesson_time = UserAvailableLessonTime(
                user=self,
            )
            available_lesson_time.save()
            return available_lesson_time

    def _get_user_related_experience_points(self) -> UserExperiencePoint:
        try:
            return self.user_experience_points
        except ObjectDoesNotExist:
            return UserExperiencePoint(
                user=self,
            )

    def _get_related_leadership_board_score(self) -> LeadershipScore:
        try:
            now = timezone.now()
            return self.leadership_board_scores.get(created_at__month=now.month, created_at__year=now.year)
        except ObjectDoesNotExist:
            leadership_score = LeadershipScore(
                user=self,
            )
            leadership_score.save()
            return leadership_score

    def _get_related_referral_credits(self) -> UserReferralCredits:
        try:
            return self.user_credits
        except ObjectDoesNotExist:
            return UserReferralCredits(
                user=self,
            )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
