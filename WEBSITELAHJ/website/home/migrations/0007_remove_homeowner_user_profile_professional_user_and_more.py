# Generated by Django 5.0.1 on 2024-02-29 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_userprofile_email_remove_userprofile_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeowner',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='professional',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
