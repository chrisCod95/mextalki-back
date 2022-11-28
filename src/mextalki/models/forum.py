import datetime

from django.db import models
from django.utils.timezone import now
from tinymce import models as tinymce_models

from src.mextalki.models.base_model import TimeStampMixin
from src.mextalki.models.utils import upload_to_v2


class Post(TimeStampMixin):
    ANNOUNCEMENT = 'AN'
    CHALLENGE = 'CH'
    BLOG_POST = 'BL'
    CONTENT_TYPE_CHOICES = [
        (ANNOUNCEMENT, 'Announcement'),
        (CHALLENGE, 'Challenge'),
        (BLOG_POST, 'Blog_post')
    ]

    content_type = models.CharField(
        max_length=2,
        choices=CONTENT_TYPE_CHOICES,
        default=ANNOUNCEMENT,
    )

    created_at = models.DateField(
        default=now,
    )

    announcement = models.OneToOneField(
        'mextalki.Announcement',
        on_delete=models.CASCADE,
        related_name='post',
        null=True,
        blank=True,
    )

    challenge = models.OneToOneField(
        'mextalki.Challenge',
        on_delete=models.CASCADE,
        related_name='post',
        null=True,
        blank=True,
    )

    blog_post = models.OneToOneField(
        'mextalki.BlogPost',
        on_delete=models.CASCADE,
        related_name='post',
        null=True,
        blank=True,
    )

    active = models.BooleanField(default=True)

    def get_content(self):
        if self.content_type == self.ANNOUNCEMENT:
            return self.announcement
        if self.content_type == self.CHALLENGE:
            return self.challenge
        if self.content_type == self.BLOG_POST:
            return self.blog_post

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return '{content_type} created at {created_at}'.format(content_type=self.content_type, created_at=self.created_at)


class Announcement(TimeStampMixin):
    created_at = models.DateTimeField(
        null=True,
        blank=True,
        default=now,
    )
    title = models.CharField(max_length=125)
    content = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    preview = tinymce_models.HTMLField(
        default='',
        blank=False,
        null=False,
    )
    active = models.BooleanField(default=True)
    file_path = 'forum_posts/announcements'
    image = models.ImageField(
        upload_to=upload_to_v2,
        default='',
        blank=True,
        null=True,
    )
    slug = models.SlugField(blank=False, null=False, default='')

    class Meta:
        verbose_name_plural = 'Forum - Announcements'

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            Post(announcement=self, content_type='AN').save()
        super().save(*args, **kwargs)

    @classmethod
    def get_last_announcements(cls):
        return cls.objects.filter(
            active=True,
            created_at__lte=datetime.datetime.today(),
            created_at__gt=datetime.datetime.today() - datetime.timedelta(days=30),
        ).order_by('-created_at')

    def __str__(self):
        return '{created_at} - {title}'.format(created_at=self.created_at, title=self.title)


class Challenge(TimeStampMixin):
    created_at = models.DateTimeField(
        null=True,
        blank=True,
        default=now,
    )
    title = models.CharField(max_length=125)
    content = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=False, null=False, default='')

    class Meta:
        verbose_name_plural = 'Forum - Challenges'

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            Post(challenge=self, content_type='CH').save()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{created_at} - {title}'.format(created_at=self.created_at, title=self.title)


class Comment(TimeStampMixin):
    created_at = models.DateTimeField(
        default=now,
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments',
        default=None,
    )
    post = models.ForeignKey(
        'mextalki.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        default=None,
    )
    content = models.TextField(
        max_length=500,
    )
    active = models.BooleanField(
        default=True,
    )
    is_challenge_correct_answer = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name_plural = 'Forum - Comments'

    def __str__(self):
        return '{user} at {post}'.format(user=self.user, post=self.post)


class Like(TimeStampMixin):
    post = models.ForeignKey(
        'mextalki.Post',
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True,
        default=None,
    )
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='likes',
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{user} at {post}'.format(user=self.user, post=self.post)


class BlogPost(TimeStampMixin):
    created_at = models.DateTimeField(
        null=True,
        blank=True,
        default=now,
    )
    title = models.CharField(max_length=125)
    content = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    preview = models.TextField()
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=False, null=False, default='')

    file_path = 'forum_posts/announcements'
    image = models.ImageField(
        upload_to=upload_to_v2,
        default='',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Forum - Blog Posts'

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            Post(blog_post=self, content_type='BL').save()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{created_at} - {title}'.format(created_at=self.created_at, title=self.title)
