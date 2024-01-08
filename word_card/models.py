from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dictionary.models import Word
from course.models import Lesson
from alerts.models import Popup,Note,Label
from course.models import ItemList
from .items import itemAddition,itemRomoval
# Create your models here.


class WordCard(models.Model):
    word = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    arrangement_number = models.IntegerField(null=True, default=0)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    dictionary = models.ForeignKey(
        Word, on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None,)
    linked  = models.BooleanField(default=False)
    popup_linked = models.ManyToManyField(Popup,blank=True)
    note_linked = models.ManyToManyField(Note,blank=True)
    label_linked = models.ManyToManyField(Label,blank=True)
    info_type = models.CharField(max_length=100,default="word_card",editable=False)
    
    
    def __str__(self):
        return self.word

    def save(self,*args, **kwargs):
        super(WordCard, self).save(*args, **kwargs)
        print("saving new item",self.id)
        itemAddition("word_card",self.lesson.id,self.id)

    def delete(self,*args, **kwargs):
        itemRomoval("word_card",self.lesson.id,self.id)
        super(WordCard, self).delete(*args, **kwargs)