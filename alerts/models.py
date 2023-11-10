from django.db import models
from course.models import Lesson
# Create your models here.



class Note(models.Model):
    title = models.CharField(max_length=200,blank=False)
    subtitle = models.CharField(max_length=250,blank=True)
    file = models.ImageField(upload_to="note_images/",blank=True)
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=True,null=True)
    info_type = models.CharField(max_length=100,default="note",editable=False)
    def __str__(self):
        return self.title




class Popup(models.Model):
    title = models.CharField(max_length=200,blank=False)
    file = models.ImageField(upload_to="popup_images/",blank=True)
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=True,null=True)
    info_type = models.CharField(max_length=100,default="popup",editable=False)
    
    def __str__(self):
        return self.title


class Label(models.Model):
    title = models.CharField(max_length=200,blank=False)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=True,null=True)
    info_type = models.CharField(max_length=100,default="label",editable=False)
    def __str__(self):
        return self.title
 