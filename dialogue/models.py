from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from course.models import Lesson
# Create your models here.
from multiselectfield import MultiSelectField


class ImageModal(models.Model):
    created = models.DateTimeField(auto_now_add=True,editable=False)
    file = models.ImageField(upload_to="dialogue_images/",blank=True)
    hints = models.CharField(max_length=100,default="")
    arrangement_number = models.IntegerField(default=0)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    info_type = models.CharField(max_length=100,default="image-modal",editable=False)
    def __str__(self):
        return self.hints

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(ImageModal, self).save(*args, **kwargs)

VOICE_CHOICES = (
    ("male_voice", "Male Voice"),
    ("female_voice", "Female Voice"),
)
class Ballon(models.Model):
    avatar = models.CharField(
            max_length = 20,
            choices = VOICE_CHOICES,
            default = 'male_voice'
            )
    file = models.FileField(upload_to="dialogue_voices/",blank=True,null=True)
    meaning = models.CharField(max_length=300,default="")
    ideogram = models.CharField(max_length=300,default="")
    pronunciation = models.CharField(max_length=300,default="",blank=True,null=True)
    arrangement_number = models.IntegerField(null=True, default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    info_type = models.CharField(max_length=100,default="balloon",editable=False)


    def __str__(self):
        return self.ideogram + " is "+ self.meaning

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Ballon, self).save(*args, **kwargs)

class Dialogue(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    dialogue_group = models.ForeignKey('DialogueGroup',on_delete=models.CASCADE,null=True)
    ballon = models.ManyToManyField(Ballon,blank=True)
    image = models.ManyToManyField(ImageModal,blank=True)
    title = models.CharField(max_length=200,default="")
    arrangement_number = models.IntegerField( default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    info_type = models.CharField(max_length=100,default="dialogue",editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(Dialogue, self).save(*args, **kwargs)



class DialogueGroup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default="")
    arrangement_number = models.IntegerField(null=True, default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    info_type = models.CharField(max_length=100,default="dialogue_group",editable=False)
    arragements = models.JSONField(default=dict({"data":False}))
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(DialogueGroup, self).save(*args, **kwargs)
        

TEST_ANSWER_CHOICES = (
    ("i", "ideogram type"),
    ("p", "Pinyin Type"),
    ("m", "Meaning Type"),
)
  

class TestAnswer(models.Model):
    
    text = models.CharField(max_length=100,default='')
    test = models.ForeignKey('TestCard',on_delete=models.CASCADE,null=True)
    answer_type = models.CharField(
            max_length = 20,
            choices = TEST_ANSWER_CHOICES,
            default = 'i'
            )
    arrangement_number = models.IntegerField(null=True, default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    info_type = models.CharField(max_length=100,default="test_answer",editable=False)
    
    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(TestAnswer, self).save(*args, **kwargs)
        


TEST_CARD_TYPE = (
    ("ideogram", "ideogram"),
    ("pinyin", "pinyin"),
)

class TestCard(models.Model):
    dialogue_group = models.ForeignKey(DialogueGroup,on_delete=models.CASCADE,null=True,blank=False)
    dialogue = models.ForeignKey(Dialogue,on_delete=models.CASCADE)
    card_type = models.CharField(
            max_length = 20,
            choices = TEST_CARD_TYPE,
            default = 'ideogram'
            )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    answers = models.ManyToManyField(TestAnswer,blank=True)
    test_text = models.TextField(blank=True, null=True)
    hide =  models.TextField(blank=True, null=True,default='')
    arrangement_number = models.IntegerField(null=True, default=0)
    created = models.DateTimeField(auto_now_add=True,editable=False)
    edited_ballon = models.ForeignKey(Ballon,on_delete=models.SET_NULL,null=True)
    last_updated = models.DateTimeField(
        blank=True, editable=False, default=timezone.now
    )
    info_type = models.CharField(max_length=100,default="test_card",editable=False)
    
    
    def __str__(self):
        return 'Test for ' + self.dialogue.title

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(TestCard, self).save(*args, **kwargs)
