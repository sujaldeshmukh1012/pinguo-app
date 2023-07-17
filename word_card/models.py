from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dictionary.models import Word
from course.models import Lesson

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
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(WordCard, self).save(*args, **kwargs)
