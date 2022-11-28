import nested_admin
from django.contrib import admin

from src.mextalki.logger import logger
from src.mextalki.models import (
    Announcement,
    Answer,
    Carousel,
    Challenge,
    Comment,
    CommonVideoScore,
    ContentListItem,
    ConversationClubInfo,
    ConversationClubSchedule,
    ConversationClubTestimonial,
    Coupon,
    Course,
    CourseGridPic,
    EventType,
    Faq,
    FaqQuestion,
    HomeCopyInfo,
    ImageLessonActivity,
    LeaderBoardRewards,
    LeadershipBoardInfo,
    LeadershipScore,
    Lesson,
    LessonActivity,
    LessonTest,
    LessonVideo,
    Level,
    Like,
    ListeningPractice,
    ListeningPracticeAudio,
    MainCopy,
    MaskCopy,
    MaskInfo,
    Module,
    ModuleInfo,
    PaypalPayment,
    Plan,
    PlanBoxItem,
    PlanPayment,
    Podcast,
    PodcastTest,
    PodcastTestAnswer,
    PodcastTestQuestion,
    Question,
    Referral,
    Reminder,
    ScheduledEvent,
    SpeakingPractice,
    SpeakingPracticeAudio,
    SpeakingPracticeResource,
    StripePayment,
    Teacher,
    TeachersReview,
    Testimonial,
    UsedCoupon,
    UsefulSpanish,
    UsefulSpanishAudio,
    Video,
    VideoScore,
    BlogPost,
)


class CourseGridPicInline(admin.TabularInline):
    model = CourseGridPic
    extra = 0
    fields = ('sort_order', 'label', 'image', 'big_size')


class ContentListItemInline(admin.TabularInline):
    model = ContentListItem
    extra = 0
    fields = ('sort_order', 'label', 'color')


class PlanBoxItemInline(admin.TabularInline):
    model = PlanBoxItem
    extra = 0
    fields = ('sort_order', 'plan', 'color')


class LessonVideoInline(admin.TabularInline):
    model = LessonVideo
    extra = 0
    fields = ('sort_order', 'url')


class SpeakingPracticeResourceInline(admin.TabularInline):
    model = SpeakingPracticeResource
    extra = 0
    fields = ('sort_order', 'title', 'url')


class SpeakingPracticeAudioInline(admin.TabularInline):
    model = SpeakingPracticeAudio
    extra = 0
    fields = ('sort_order', 'title', 'description', 'file')


class ListeningPracticeAudioInline(admin.TabularInline):
    model = ListeningPracticeAudio
    extra = 0
    fields = ('sort_order', 'title', 'transcription', 'answer', 'file')


class UsefulSpanishAudioInline(admin.TabularInline):
    model = UsefulSpanishAudio
    extra = 0
    fields = ('sort_order', 'title', 'description', 'file')


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = (
        'title', 'type', 'get_course', 'module', 'active', 'free',
        'type', 'created_at', 'updated_at',
    )
    list_display_links = ('title', 'module')
    list_filter = (
        'active',
        'free',
        'module',
        'type',
    )
    search_fields = ('title',)
    ordering = ('module__level__course', 'module', 'sort_order')

    def get_course(self, obj):
        try:
            return obj.module.course
        except Exception as error:
            logger.error(error)
            return ''

    get_course.short_description = 'Course'
    get_course.admin_order_field = 'course__id'

    inlines = (LessonVideoInline,)


class LevelAdminInline(admin.TabularInline):
    model = Level
    extra = 0
    fields = ('title', 'sort_order')
    readonly_fields = ('title',)
    show_change_link = True


class CustomCourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('title', 'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    search_fields = ('title', 'subtitle')
    ordering = ('id',)
    inlines = (
        CourseGridPicInline, ContentListItemInline,
        PlanBoxItemInline, LevelAdminInline,
    )


class CustomPlanAdmin(admin.ModelAdmin):
    model = Plan
    list_display = (
        'title', 'course', 'price', 'currency', 'active', 'created_at', 'updated_at',
    )
    list_display_links = ('title', 'course')
    search_fields = ('title', 'price')
    list_filter = ('active', 'currency')


class CustomPlanPaymentAdmin(admin.ModelAdmin):
    model = PlanPayment
    list_display = ('id', 'user', 'plan', 'paypal_payment', 'created_at', 'updated_at')
    list_filter = ('plan',)
    list_display_links = ('id', 'user', 'plan', 'paypal_payment')


class CustomPaypalPaymentAdmin(admin.ModelAdmin):
    model = PaypalPayment
    list_display = (
        'id', 'intent', 'status',
        'payer_email', 'created_at', 'updated_at',
    )
    list_filter = ('status', 'intent')
    list_display_links = ('id',)


class CustomStripePaymentAdmin(admin.ModelAdmin):
    model = StripePayment
    list_display = (
        'id',
        'subscription_id',
        'customer_id',
        'charge_id',
        'status',
        'billing_reason',
        'currency',
        'customer_email',
        'created_at',
        'updated_at',
    )
    list_filter = ('status',)
    list_display_links = ('id',)


class CustomSpeakingPracticeAdmin(admin.ModelAdmin):
    model = SpeakingPractice
    list_display = ('__str__', 'get_module', 'get_course')
    ordering = ('id',)

    def get_module(self, obj):
        try:
            return obj.lesson.module
        except Exception as error:
            logger.error(error)
            return ''

    get_module.short_description = 'Module'
    get_module.admin_order_field = 'module__id'

    def get_course(self, obj):
        try:
            return obj.lesson.module.course
        except Exception as error:
            logger.error(error)
            return ''

    get_course.short_description = 'Course'
    get_course.admin_order_field = 'course__id'

    inlines = (SpeakingPracticeResourceInline, SpeakingPracticeAudioInline)


class LessonAdminInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('title', 'sort_order')
    readonly_fields = ('title',)
    show_change_link = True


class CustomModuleAdmin(admin.ModelAdmin):
    model = Module
    list_display = ('title', 'level')
    list_filter = ('level',)
    list_display_links = ('title', 'level')
    ordering = ('id',)
    inlines = (LessonAdminInline,)


class ModuleAdminInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('title', 'sort_order')
    readonly_fields = ('title',)
    show_change_link = True


class LevelAdmin(admin.ModelAdmin):
    model = Level
    list_display = ('title', 'course')
    list_filter = ('course',)
    list_display_links = ('title', 'course')
    inlines = (ModuleAdminInline,)


class CustomListeningPracticeAdmin(admin.ModelAdmin):
    model = ListeningPractice
    ordering = ('id',)
    inlines = (ListeningPracticeAudioInline,)


class CustomUsefulSpanishAdmin(admin.ModelAdmin):
    model = UsefulSpanish
    list_display = ('id', 'lesson')
    list_display_links = ('id', 'lesson')
    ordering = ('id',)
    inlines = (UsefulSpanishAudioInline,)


class CustomModuleInfoAdmin(admin.ModelAdmin):
    model = ModuleInfo
    list_display = ('id', 'lesson')
    list_display_links = ('id', 'lesson')
    ordering = ('id',)


class CustomTestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ('name', 'active')
    list_display_links = ('name',)
    list_filter = ('active',)
    ordering = ('id',)


class CustomTeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ('name', 'active', 'time_zone', 'created_at', 'updated_at')
    list_display_links = ('name',)


class CustomCarouselItemAdmin(admin.ModelAdmin):
    model = Carousel
    list_display = ('title', 'active')
    list_display_links = ('title',)
    list_filter = ('active',)
    ordering = ('id',)


class CustomScheduledEventAdmin(admin.ModelAdmin):
    model = ScheduledEvent
    list_display = (
        'id',
        'user',
        'event_type',
        'teacher',
        'start_time',
        'end_time',
        'time_zone',
        'status',
        'provider',
        'location',
        'provider_event_id',
        'provider_invite_id',
        'created_at',
        'updated_at',
    )
    list_display_links = ('id', 'user', 'event_type', 'teacher')
    list_filter = ('teacher', 'event_type')
    search_fields = ('provider_event_id', 'provider_invite_id')


class CustomEventTypeAdmin(admin.ModelAdmin):
    model = EventType
    list_display = (
        'title',
        'active',
        'teacher',
        'type',
        'event_duration',
        'calendar_url',
        'created_at',
        'updated_at',
    )
    list_display_links = ('title',)


class PodcastAdmin(admin.ModelAdmin):
    model = Podcast
    list_display = (
        'title', 'slug', 'sort_order', 'active',
    )
    ordering = ('sort_order',)


class HomeCopyInfoAdmin(admin.ModelAdmin):
    model = HomeCopyInfo


class MainCopyAdmin(admin.ModelAdmin):
    model = MainCopy


class ConversationClubTestimonialAdmin(admin.TabularInline):
    model = ConversationClubTestimonial
    extra = 0
    fields = (
        'sort_order', 'language', 'active', 'thumbnail',
        'flag_thumbnail', 'testimonial_video_url',
    )


class ConversationClubScheduleAdmin(admin.TabularInline):
    model = ConversationClubSchedule
    extra = 0


class ConversationClubCopyAdmin(admin.ModelAdmin):
    model = ConversationClubInfo
    inlines = (ConversationClubScheduleAdmin, ConversationClubTestimonialAdmin)


class CustomAnswerItemAdmin(nested_admin.NestedStackedInline):
    model = Answer
    extra = 0


class CustomQuestionItemAdmin(nested_admin.NestedStackedInline):
    model = Question
    extra = 0
    inlines = [CustomAnswerItemAdmin]


class CustomTestAdmin(nested_admin.NestedModelAdmin):
    model = LessonTest
    inlines = (CustomQuestionItemAdmin,)


class FaqQuestionAdmin(admin.TabularInline):
    model = FaqQuestion
    extra = 0


class FaqAdmin(admin.ModelAdmin):
    model = Faq
    inlines = (FaqQuestionAdmin,)


class CustomPodcastAnswerItemAdmin(nested_admin.NestedStackedInline):
    model = PodcastTestAnswer
    extra = 0


class CustomPodcastQuestionItemAdmin(nested_admin.NestedStackedInline):
    model = PodcastTestQuestion
    extra = 0
    inlines = [CustomPodcastAnswerItemAdmin]


class CustomPodcastTestItemAdmin(nested_admin.NestedModelAdmin):
    model = PodcastTest
    inlines = [CustomPodcastQuestionItemAdmin]


class MaskInfoAdmin(admin.TabularInline):
    model = MaskInfo
    extra = 0


class MaskCopyAdmin(admin.ModelAdmin):
    model = MaskCopy
    inlines = (MaskInfoAdmin,)


class CouponAdmin(admin.ModelAdmin):
    model = Coupon
    list_display = (
        'code',
        'owner',
        'active',
        'discount',
        'times_used',
        'times_used_limit',
        'is_for_limited_time',
        'limited_time',
        'created_at',
        'updated_at',
    )
    search_fields = ('code',)
    list_filter = ('active',)


class USedCouponAdmin(admin.ModelAdmin):
    model = UsedCoupon
    list_display = (
        'user',
        'coupon',
        'created_at',
        'updated_at',
    )


class TeachersTestimonialAdmin(admin.ModelAdmin):
    model = TeachersReview


class LeadershipPointsAdmin(admin.ModelAdmin):
    model = LeadershipScore
    ordering = ('-exp_points', '-created_at')


class LeadershipBoardInfoAdmin(admin.ModelAdmin):
    model = LeadershipBoardInfo


class VideoScoreAdmin(admin.ModelAdmin):
    model = VideoScore
    list_display = (
        'exp_points',
        'user',
        'podcast',
        'created_at',
        'updated_at',
    )


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = (
        'title', 'slug', 'sort_order', 'active',
    )
    ordering = ('sort_order',)


class CommonVideoScoreAdmin(admin.ModelAdmin):
    model = CommonVideoScore
    list_display = (
        'exp_points',
        'user',
        'video',
        'created_at',
        'updated_at',
    )


class ReferralAdmin(admin.ModelAdmin):
    model = Referral
    readonly_fields = ['code']

    list_display = (
        'id', 'user', 'code', 'recommended_by', 'purchased_plan', 'earned_credits',
    )
    ordering = ('id',)


class LeaderBoardRewardsAdmin(admin.ModelAdmin):
    model = LeaderBoardRewards


class AnnouncementAdmin(admin.ModelAdmin):
    model = Announcement


class CommentAdmin(admin.ModelAdmin):
    model = Comment


class ChallengeAdmin(admin.ModelAdmin):
    model = Challenge


class LikeAdmin(admin.ModelAdmin):
    model = Like


class ImageLessonActivityInline(admin.TabularInline):
    model = ImageLessonActivity
    fields = ('image', 'image_url')
    readonly_fields = ('image_url',)
    extra = 0


class LessonActivityAdmin(admin.ModelAdmin):
    model = LessonActivity
    inlines = (ImageLessonActivityInline,)


class ScheduledEventReminderAdmin(admin.ModelAdmin):
    model = Reminder
    list_display = ('id', 'user', 'event_status', 'reminder_schedule',
                    'reminder_was_sent', 'scheduled_event')


class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost


admin.site.register(LeaderBoardRewards, LeaderBoardRewardsAdmin)
admin.site.register(HomeCopyInfo, HomeCopyInfoAdmin)
admin.site.register(MainCopy, MainCopyAdmin)
admin.site.register(Course, CustomCourseAdmin)
admin.site.register(Plan, CustomPlanAdmin)
admin.site.register(PlanPayment, CustomPlanPaymentAdmin)
admin.site.register(PaypalPayment, CustomPaypalPaymentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Module, CustomModuleAdmin)
admin.site.register(SpeakingPractice, CustomSpeakingPracticeAdmin)
admin.site.register(ListeningPractice, CustomListeningPracticeAdmin)
admin.site.register(UsefulSpanish, CustomUsefulSpanishAdmin)
admin.site.register(ModuleInfo, CustomModuleInfoAdmin)
admin.site.register(Testimonial, CustomTestimonialAdmin)
admin.site.register(Carousel, CustomCarouselItemAdmin)
admin.site.register(Teacher, CustomTeacherAdmin)
admin.site.register(StripePayment, CustomStripePaymentAdmin)
admin.site.register(ScheduledEvent, CustomScheduledEventAdmin)
admin.site.register(EventType, CustomEventTypeAdmin)
admin.site.register(ConversationClubInfo, ConversationClubCopyAdmin)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(LessonTest, CustomTestAdmin)
admin.site.register(PodcastTest, CustomPodcastTestItemAdmin)
admin.site.register(MaskCopy, MaskCopyAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(UsedCoupon, USedCouponAdmin)
admin.site.register(TeachersReview, TeachersTestimonialAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(LeadershipScore, LeadershipPointsAdmin)
admin.site.register(LeadershipBoardInfo, LeadershipBoardInfoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoScore, VideoScoreAdmin)
admin.site.register(CommonVideoScore, CommonVideoScoreAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(LessonActivity, LessonActivityAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reminder, ScheduledEventReminderAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
