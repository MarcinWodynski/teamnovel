# Generated by Django 2.2.6 on 2020-06-07 07:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novels', '0012_publishednovel_publish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishednovel',
            name='user_ratings',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
