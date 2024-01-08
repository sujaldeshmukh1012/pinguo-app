# Generated by Django 4.2.3 on 2024-01-05 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dialogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DGItemListMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('dialogue', 'dialogue'), ('test_card', 'test_card')], max_length=20)),
                ('item_id', models.PositiveIntegerField()),
                ('dialogue_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialogue.dialoguegroup')),
            ],
        ),
    ]
