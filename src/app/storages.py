from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


def static_storage(): return S3Boto3Storage(location=settings.STATIC_FILES_LOCATION)


def media_storage(): return S3Boto3Storage(location=settings.MEDIA_FILES_LOCATION)
