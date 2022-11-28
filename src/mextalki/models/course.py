from colorfield.fields import ColorField
from django.db import models
from sort_order_field import SortOrderField
from tinymce import models as tinymce_models

from .base_model import TimeStampMixin
from .utils import upload_image_to, upload_thumbnail_to


class Course(TimeStampMixin):
    color = ColorField(default='#FFFFFF')
    slug = models.SlugField(blank=False, null=False, default='')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    home_description = models.TextField(default='')
    file_path = 'courses/thumbnail'
    thumbnail = models.ImageField(upload_to=upload_thumbnail_to, default='')
    video = models.URLField(blank=True, null=False, default='')
    active = models.BooleanField(
        default=True,
    )
    learn_description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )
    grid_description = models.TextField(max_length=500, blank=True, null=True)

    course_extend_description = tinymce_models.HTMLField(
        default='',
        blank=True,
        null=True,
    )

    @classmethod
    def get_active_courses(cls):
        return cls.objects.filter(active=True).order_by('created_at')

    def get_grid_pics(self):
        return self.grid_pics.all()

    def get_content_list(self):
        return self.content_list.all()

    def get_plan_box_items(self):
        return self.plan_list.all()

    def get_levels(self):
        return self.levels.all()

    def __str__(self):
        return '{title} {subtitle}'.format(title=self.title, subtitle=self.subtitle)


class CourseGridPic(models.Model):
    course = models.ForeignKey(
        'mextalki.Course',
        on_delete=models.CASCADE,
        related_name='grid_pics',
    )
    sort_order = SortOrderField()
    label = models.CharField(max_length=100)
    file_path = 'courses/grid_pics'
    image = models.ImageField(upload_to=upload_image_to)
    big_size = models.BooleanField(default=False)

    def __str__(self):
        return '{image_name}'.format(image_name=self.image.name)

    class Meta:
        ordering = ('sort_order',)


class ContentListItem(models.Model):
    course = models.ForeignKey(
        'mextalki.Course',
        on_delete=models.CASCADE,
        related_name='content_list',
    )
    sort_order = SortOrderField()
    color = ColorField(default='#FFFFFF')
    label = models.CharField(max_length=100)

    def __str__(self):
        return '{label}'.format(label=self.label)

    class Meta:
        ordering = ('sort_order',)


class PlanBoxItem(models.Model):
    course = models.ForeignKey(
        'mextalki.Course',
        on_delete=models.CASCADE,
        related_name='plan_list',
    )
    sort_order = SortOrderField()
    color = ColorField(default='#FFFFFF')
    plan = models.ForeignKey(
        'mextalki.Plan',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    def __str__(self):
        return '{label}'.format(label=self.plan.title)

    class Meta:
        ordering = ('sort_order',)


class Level(TimeStampMixin):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        'mextalki.Course',
        on_delete=models.PROTECT,
        related_name='levels',
        blank=False,
        null=False,
    )
    sort_order = SortOrderField()

    def get_modules(self):
        return self.modules.all()

    def __str__(self):
        return '{course} - {title}'.format(title=self.title, course=self.course.title)

    class Meta:
        ordering = ('sort_order',)
        verbose_name = 'Course - Level'
        verbose_name_plural = 'Courses - Levels'


class Module(TimeStampMixin):
    title = models.CharField(max_length=255)
    level = models.ForeignKey(
        'mextalki.Level',
        on_delete=models.PROTECT,
        related_name='modules',
        blank=True,
        null=True,
        default=None,
    )

    def get_lessons(self):
        return self.lessons.filter(active=True)

    sort_order = SortOrderField()

    def __str__(self):
        return '{level} - {title}'.format(title=self.title, level=self.level.title)

    class Meta:
        ordering = ('sort_order',)
        verbose_name = 'Course - Modules'
        verbose_name_plural = 'Courses - Modules'


class Lesson(TimeStampMixin):
    color = ColorField(default='#FFFFFF')
    white_font = models.BooleanField(default=False)
    slug = models.SlugField(blank=False, null=False, default='')
    title = models.CharField(max_length=255)
    link_title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField(
        blank=True,
        null=True,
    )
    content_description = models.TextField(blank=True, null=True)
    TYPE_CHOICES = [
        ('LESSON', 'LESSON'),
        ('MODULE', 'MODULE'),
    ]
    active = models.BooleanField(
        default=True,
    )
    free = models.BooleanField(
        default=False,
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=20)
    module = models.ForeignKey(
        'mextalki.Module',
        on_delete=models.CASCADE,
        related_name='lessons',
        blank=True,
        null=True,
    )
    sort_order = SortOrderField()

    def get_videos(self):
        return self.videos.all()

    def __str__(self):
        return self.title

    @property
    def main_test(self):
        return self.tests.first()

    class Meta:
        ordering = ('sort_order',)
        verbose_name = 'Course - Lesson'
        verbose_name_plural = 'Courses - Lessons'
