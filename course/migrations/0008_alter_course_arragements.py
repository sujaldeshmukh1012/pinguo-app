# Generated by Django 4.2.3 on 2023-12-14 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_lesson_arragements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='arragements',
            field=models.JSONField(default={'data': False}),
        ),
    ]