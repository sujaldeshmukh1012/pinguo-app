from django.db import models
from django.utils import timezone

# Create your models here.


class Word(models.Model):
    meaning = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    ideogram = models.CharField(max_length=100, blank=True)
    pronunciation = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    HSK = models.PositiveIntegerField(blank=True)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    arrangement_number = models.IntegerField(null=True, default=0)
    male_voice = models.FileField(
        upload_to="audio/male_voices", blank=True, null=True, default=None
    )
    female_voice = models.FileField(
        upload_to="audio/female_voices", blank=True, null=True, default=None
    )
    info_type = models.CharField(max_length=100,default="word",editable=False)

    def __str__(self):
        return self.ideogram + " is " + self.meaning

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        self.arrangement_number = self.arrangement_number + 1
        super(Word, self).save(*args, **kwargs)


class Hanzi(models.Model):
    word = models.CharField(max_length=100,blank=False)
    video = models.FileField(upload_to="hanzi-videos/",blank=True)
    image = models.ImageField(upload_to="hanzi-images/",blank=True)
    subtitle = models.CharField(max_length=100,blank=True)
    meaning = models.CharField(max_length=100,blank=True)
    pinyin = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    sub_description = models.TextField(blank=True)
    hsk=models.IntegerField(default=1,blank=True)
    strokes_no=models.IntegerField(default=3,blank=True)
    
    
class ToneType(models.Model):
    title= models.CharField(max_length=100,blank=False)
    pinyin_text= models.CharField(max_length=100,blank=True)
    subheader = models.CharField(max_length=100,blank=True)
    description= models.TextField(blank=False)
    female_voice = models.FileField(upload_to="ToneTypes/female/",blank=True)
    male_voice = models.FileField(upload_to="ToneTypes/male/",blank=True)
    
class ToneNotes(models.Model):
    tone_text = models.CharField(max_length=100,blank=False)
    image = models.FileField(upload_to="PinyinTone/tone-images/",blank=False)
    female_voice = models.FileField(upload_to="ToneNotes/female/")
    male_voice = models.FileField(upload_to="ToneNotes/male/")
    
class PinyinTone(models.Model):
    title = models.CharField(max_length=150,blank=True)
    tone_no =  models.ManyToManyField(ToneType)
    toneNotes = models.ManyToManyField(ToneNotes)
    
    
class PinyinInitialAndFinal(models.Model):
    title= models.CharField(max_length=100,blank=False)
    initial = models.ForeignKey(ToneType,on_delete=models.CASCADE,related_name="Initial")
    final = models.ForeignKey(ToneType,on_delete=models.CASCADE)

class Pinyin(models.Model):
    tone = models.ForeignKey(PinyinTone,on_delete=models.CASCADE)
    initial_and_final = models.ForeignKey(PinyinInitialAndFinal,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tone