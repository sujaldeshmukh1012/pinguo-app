# Generated by Django 4.2.3 on 2023-10-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_hanzi_tonenotes_tonetype_pinyintone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hanzi',
            name='image',
            field=models.ImageField(blank=True, upload_to='hanzi-images/'),
        ),
        migrations.AddField(
            model_name='hanzi',
            name='meaning',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='hanzi',
            name='video',
            field=models.FileField(blank=True, upload_to='hanzi-videos/'),
        ),
    ]