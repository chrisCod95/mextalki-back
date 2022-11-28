from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class TesUserValidations(TestCase):

    def setUp(self):
        self.password = 'password_456'
        self.first_name = 'Jane'
        self.last_name = 'Doe'

    def test_email_validation(self):
        """email validation of the User model"""

        with self.assertRaises(ValueError):
            USER_MODEL.objects.create_user(
                email=None,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                username='user_123',
            )

    def test_email_unique(self):
        """email unique attr of the User model"""

        duplicated_email = 'jane@mail.com'

        with self.assertRaises(IntegrityError):
            USER_MODEL.objects.create_user(
                email=duplicated_email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                username='jane123',
            )

            USER_MODEL.objects.create_user(
                email=duplicated_email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                username='jane1234',
            )

    def test_username_unique(self):
        """username unique attr of the User model"""

        duplicated_username = 'jane123'

        with self.assertRaises(IntegrityError):
            USER_MODEL.objects.create_user(
                email='jane123@mail.com',
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                username=duplicated_username,
            )

            USER_MODEL.objects.create_user(
                email='jane1234@mail.com',
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                username=duplicated_username,
            )
