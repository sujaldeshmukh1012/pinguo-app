# Generated by Django 4.2.3 on 2024-01-05 20:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hanzi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('video', models.FileField(blank=True, upload_to='hanzi-videos/')),
                ('image', models.ImageField(blank=True, upload_to='hanzi-images/')),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('meaning', models.CharField(blank=True, max_length=100)),
                ('pinyin', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('sub_description', models.TextField(blank=True)),
                ('hsk', models.IntegerField(blank=True, default=1)),
                ('strokes_no', models.IntegerField(blank=True, default=3)),
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
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.CharField(blank=True, max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('ideogram', models.CharField(blank=True, max_length=100)),
                ('pronunciation', models.CharField(blank=True, max_length=100)),
                ('text', models.TextField(blank=True)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('HSK', models.PositiveIntegerField(blank=True)),
                ('last_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('arrangement_number', models.IntegerField(default=0, null=True)),
                ('male_voice', models.FileField(blank=True, default=None, null=True, upload_to='audio/male_voices')),
                ('female_voice', models.FileField(blank=True, default=None, null=True, upload_to='audio/female_voices')),
                ('info_type', models.CharField(default='word', editable=False, max_length=100)),
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
