# Generated by Django 4.2.3 on 2023-12-13 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_info_type_lesson_info_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='arragements',
            field=models.JSONField(default={'items': []}),
        ),
        migrations.AddField(
            model_name='lesson',
            name='arragements',
            field=models.JSONField(default={'items': []}),
        ),
    ]