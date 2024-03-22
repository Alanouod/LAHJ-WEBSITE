# Generated by Django 5.0.1 on 2024-03-19 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_previouswork_products_used_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimage',
            name='professional_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='projectimage',
            name='professional_profile_link',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
