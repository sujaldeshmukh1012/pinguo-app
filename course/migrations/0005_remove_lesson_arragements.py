# Generated by Django 4.2.3 on 2023-12-13 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_arragements_lesson_arragements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='arragements',
        ),
    ]