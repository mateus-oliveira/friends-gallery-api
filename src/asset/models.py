import random
from django.db import models
from .utils import resize_and_crop_file


def upload_directory_path(instance, filename):
    HASH = random.getrandbits(100)
    return f'{HASH}-{filename}'


class Asset(models.Model):
    file = models.FileField(
        upload_to=upload_directory_path,
        blank=False,
        null=False,
    )
    uploaded_at = models.DateTimeField('Uploaded at', auto_now_add=True)

    def __str__(self):
        return f'Image {self.id}: <{self.file}>'
    
    def save(self, *args, **kwargs):
        self.file = resize_and_crop_file(self.file)
        super(Asset, self).save(*args, **kwargs)
