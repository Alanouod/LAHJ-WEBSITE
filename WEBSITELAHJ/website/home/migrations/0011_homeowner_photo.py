# Generated by Django 5.0.1 on 2024-03-04 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_userprofile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeowner',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='homeowner_photos/'),
        ),
    ]