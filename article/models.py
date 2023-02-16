from django.db import models
import os
import uuid
from django.core.validators import FileExtensionValidator
from helpers.models import TrakingModel
from article.validators import validate_file_size
from authentification.models import User
# Create your models here.


class Articles(TrakingModel):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    description = models.TextField()
    added_by = models.ForeignKey(
        User, related_name='articles', on_delete=models.CASCADE, blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name='articles_updated', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.code} - {self.added_by}'


class Picture(TrakingModel):

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('documents/', filename)

    title = models.CharField(max_length=25)
    file = models.ImageField(
        upload_to=get_file_path,
        max_length=100, blank=True,
        validators=[validate_file_size,
                    FileExtensionValidator(['jpg', 'png', 'jpeg'])]
    )

    article = models.ForeignKey(
        Articles, related_name='images', on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return self.title
