# Generated by Django 2.2.6 on 2020-05-24 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='novel',
        ),
        migrations.AddField(
            model_name='novel',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='novels.Team'),
            preserve_default=False,
        ),
    ]
