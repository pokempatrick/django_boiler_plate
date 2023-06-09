# Generated by Django 4.1.6 on 2023-04-02 23:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='deposit',
            field=models.IntegerField(verbose_name=django.core.validators.MinValueValidator(0, message='The value should be greater than 0')),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='statut',
            field=models.CharField(choices=[('CREATE', 'created'), ('REJECT', 'rejected'), ('VALIDATE', 'validated'), ('DELETE', 'deleted')], default='CREATED', error_messages='The value is not supported', max_length=150),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='table',
            field=models.IntegerField(verbose_name=django.core.validators.MinValueValidator(0, message='The value should be greater than 0')),
        ),
        migrations.CreateModel(
            name='Validations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('statut', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validations', to='reservations.reservations')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
