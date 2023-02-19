# Generated by Django 4.1.6 on 2023-02-18 15:26

import article.models
import article.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_alter_picture_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='file',
            field=models.ImageField(blank=True, upload_to=article.models.Picture.get_file_path, validators=[article.validators.validate_file_size, django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])]),
        ),
    ]
