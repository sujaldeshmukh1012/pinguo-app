# Generated by Django 4.2.3 on 2024-01-07 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
        ('dialogue', '0003_dgitemlistmain_d_object_dgitemlistmain_tc_object'),
        ('word_card', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlist',
            name='dg_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dialogue.dialoguegroup'),
        ),
        migrations.AddField(
            model_name='itemlist',
            name='l_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alerts.label'),
        ),
        migrations.AddField(
            model_name='itemlist',
            name='n_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alerts.note'),
        ),
        migrations.AddField(
            model_name='itemlist',
            name='pu_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alerts.popup'),
        ),
        migrations.AddField(
            model_name='itemlist',
            name='wc_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='word_card.wordcard'),
        ),
    ]
