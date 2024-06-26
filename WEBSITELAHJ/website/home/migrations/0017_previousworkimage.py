# Generated by Django 5.0.1 on 2024-03-14 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_professional_previous_work_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviousWorkImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='previous_work_images/')),
                ('previous_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.previouswork')),
            ],
        ),
    ]
