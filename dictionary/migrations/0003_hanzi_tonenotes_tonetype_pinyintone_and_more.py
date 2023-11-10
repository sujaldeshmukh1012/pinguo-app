# Generated by Django 4.2.3 on 2023-10-09 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_word_info_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hanzi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('video', models.FileField(blank=True, upload_to='hanzi/')),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('pinyin', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('sub_description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ToneNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tone_text', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='PinyinTone/tone-images/')),
                ('female_voice', models.FileField(upload_to='ToneNotes/female/')),
                ('male_voice', models.FileField(upload_to='ToneNotes/male/')),
            ],
        ),
        migrations.CreateModel(
            name='ToneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pinyin_text', models.CharField(blank=True, max_length=100)),
                ('subheader', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField()),
                ('female_voice', models.FileField(blank=True, upload_to='ToneTypes/female/')),
                ('male_voice', models.FileField(blank=True, upload_to='ToneTypes/male/')),
            ],
        ),
        migrations.CreateModel(
            name='PinyinTone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('toneNotes', models.ManyToManyField(to='dictionary.tonenotes')),
                ('tone_no', models.ManyToManyField(to='dictionary.tonetype')),
            ],
        ),
        migrations.CreateModel(
            name='PinyinInitialAndFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('final', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.tonetype')),
                ('initial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Initial', to='dictionary.tonetype')),
            ],
        ),
        migrations.CreateModel(
            name='Pinyin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_and_final', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.pinyininitialandfinal')),
                ('tone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.pinyintone')),
            ],
        ),
    ]
