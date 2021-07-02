from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_ROOT
    file_overwrite = False
    custom_domain = False


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIA_ROOT
    file_overwrite = False
    custom_domain = False
