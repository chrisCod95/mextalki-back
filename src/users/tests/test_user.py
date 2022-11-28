from django.test import TestCase
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

EMPTY_STR = ''


class TestUserAttributes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            email='jane@mail.com',
            first_name='Jane',
            last_name='Doe',
            username='jane_doe',
            password='password_456'
        )

    def test_str(self):
        """__str__ attr of the User model"""

        self.assertEqual(str(self.user), 'jane@mail.com')

    def test_slug(self):
        """slug attr of the User model"""

        self.assertEqual(self.user.slug, 'jane_doe')

    def test_bio(self):
        """bio attr of the User model"""

        self.assertEqual(self.user.bio, EMPTY_STR)

    def test_location(self):
        """location attr of the User model"""

        self.assertEqual(self.user.location, EMPTY_STR)

    def test_birth_day(self):
        """birth_day attr of the User model"""

        self.assertEqual(self.user.birth_day, None)

    def test_verified(self):
        """verified attr of the User model"""

        self.assertFalse(self.user.verified)

    def test_profile_picture(self):
        """profile_picture attr of the User model"""

        self.assertEqual(self.user.profile_picture, None)

    def test_payment_courses(self):
        """payment_courses property of the User model"""

        self.assertQuerysetEqual(self.user.payment_courses, [])

    def test_subscription_courses(self):
        """subscription_courses property of the User model"""

        self.assertQuerysetEqual(self.user.subscription_courses, [])

    def test_courses(self):
        """courses property of the User model"""

        self.assertQuerysetEqual(self.user.courses, [])

    def test_last_subscription(self):
        """last_subscription property of the User model"""

        self.assertEqual(self.user.last_subscription, None)

    def test_has_active_subscription(self):
        """has_active_subscription property of the User model"""

        self.assertFalse(self.user.has_active_subscription)

    def test_has_access_to_courses(self):
        """has_access_to_courses property of the User model"""

        self.assertFalse(self.user.has_access_to_courses)

    def test_total_lesson_time(self):
        """total_lesson_time property of the User model"""

        self.assertEqual(self.user.total_lesson_time, 0)

    def test_total_practice_time(self):
        """total_practice_time property of the User model"""

        self.assertEqual(self.user.total_practice_time, 0)

    def test_total_available_conversation_club_slots(self):
        """total_available_conversation_club_slots property of the User model"""

        self.assertEqual(self.user.total_available_conversation_club_slots, 0)
