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

    def __str__(self):
        return self.ideogram + " is " + self.meaning

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        self.arrangement_number = self.arrangement_number + 1
        super(Word, self).save(*args, **kwargs)
