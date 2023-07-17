from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


# class WordCard(models.Model):


class Lesson(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_course = models.ForeignKey("Course", on_delete=models.CASCADE, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(blank=True, editable=False)
    arrangement_number = models.IntegerField(null=True, default=0)

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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Course, self).save(*args, **kwargs)
