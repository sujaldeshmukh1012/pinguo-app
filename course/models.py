from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

# Create your models here.


# class WordCard(models.Model):


class Lesson(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_course = models.ForeignKey("Course", on_delete=models.CASCADE, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(blank=True, editable=False)
    arrangement_number = models.IntegerField(null=True, default=0)
    info_type = models.CharField(max_length=100,default="lesson",editable=False)
    arrangement = models.JSONField(default=list,null=True,blank=True,)


    def set_arrangement(self, list_of_ids):
        self.arrangement = list_of_ids

    def get_arrangement(self):
        return self.arrangement
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Lesson, self).save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(blank=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    arrangement_number = models.IntegerField(null=True, default=0)
    info_type = models.CharField(max_length=100,default="course",editable=False)
    arrangements = models.JSONField(null=True,blank=True,default=dict({"data":False}))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Course, self).save(*args, **kwargs)
 
 
TYPE_CHOICES=[
    ('word_card','word_card'),
    ('dialogue_group','dialogue_group'),
    ('label','label'),
    ('note','note'),
    ('popup','popup'),
    ]
class ItemList(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    item_id = models.PositiveIntegerField(unique=False)
    # wc_object = models.ForeignKey("word_card.WordCard",on_delete=models.CASCADE,null=True,blank=True)
    # dg_object = models.ForeignKey("dialogue.DialogueGroup",on_delete=models.CASCADE,null=True,blank=True)
    # l_object = models.ForeignKey("alerts.Label",on_delete=models.CASCADE,null=True,blank=True)
    # n_object = models.ForeignKey("alerts.Note",on_delete=models.CASCADE,null=True,blank=True)
    # pu_object = models.ForeignKey("alerts.Popup",on_delete=models.CASCADE,null=True,blank=True)
    # last_updated = models.DateTimeField(blank=True, editable=False)

    def __str__(self):
        return self.type + ' of id ' + str(self.item_id) + ' in lesson ' + self.lesson.title
    def save(self, *args, **kwargs):
        super(ItemList,self).save(*args, **kwargs)
        # self.last_updated = timezone.now()
        AddorKeepItem(self.id,self.lesson.id)
        return self.id
    def delete(self, *args, **kwargs):
        print("deleting")
        RemoveItem(self.id,self.lesson.id)
        super(ItemList,self).delete(*args, **kwargs)
    
def AddorKeepItem(item_id,obj):
    object_ = Lesson.objects.filter(id=obj).first()
    int_array= object_.get_arrangement()
    for id in int_array:
        if item_id == id:
            return
    print(int_array)
    int_array.append(item_id)
    object_.arrangements = int_array
    object_.save()
    return

def RemoveItem(item_id,obj):
    object_ = Lesson.objects.filter(id=obj).first()
    int_array= object_.get_arrangement()
    index = int_array.index(item_id)
    if index == -1:
        print("item does not exixts in the lesson arrangement")
        return
    int_array.pop(index)
    object_.arrangements = ",".join(int_array)
    object_.save()  
    return