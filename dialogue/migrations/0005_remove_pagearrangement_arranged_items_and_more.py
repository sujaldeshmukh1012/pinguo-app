# Generated by Django 4.2.3 on 2023-12-13 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogue', '0004_arrangeditem_pagearrangement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagearrangement',
            name='arranged_items',
        ),
        migrations.AddField(
            model_name='dialoguegroup',
            name='arragement',
            field=models.JSONField(default=''),
        ),
        migrations.DeleteModel(
            name='ArrangedItem',
        ),
        migrations.DeleteModel(
            name='PageArrangement',
        ),
    ]