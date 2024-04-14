# Generated by Django 5.0.1 on 2024-04-13 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_alter_rating_comment_alter_rating_professional_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='cumulative_rating',
        ),
        migrations.RemoveField(
            model_name='professional',
            name='total_ratings',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='professional',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.AddField(
            model_name='rating',
            name='stars',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.TextField(),
        ),
    ]
