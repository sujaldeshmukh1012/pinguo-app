from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from course.models import Lesson
# Create your models here.
from multiselectfield import MultiSelectField
from word_card.items import itemAddition,itemRomoval





def DGItemAddition(type,lesson,id):
    l = DialogueGroup.objects.filter(id=lesson).first()
    item,created = DGItemListMain.objects.get_or_create(type=type,dialogue_group=l,item_id=id)
    print("Item Addition called===========>")
    item.save()
    return True

def DGItemRomoval(type,lesson,id):
    print("Item Deletion called===========> for",type," of type and id ",id)
    l = DialogueGroup.objects.filter(id=lesson).first()
    item = DGItemListMain.objects.get(type=type,dialogue_group=l,item_id=id)
    item.delete()
    return True     


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
        DGItemAddition("dialogue",self.dialogue_group.id,self.id)

    def delete(self,*args, **kwargs):
        DGItemRomoval("dialogue",self.dialogue_group.id,self.id)
        super(Dialogue, self).delete(*args, **kwargs)
                



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
    arrangement = models.JSONField(default=list,null=True,blank=True,)
    
    def __str__(self):
        return self.title
    
    def set_arrangement(self, list_of_ids):
        self.arrangement = list_of_ids

    def get_arrangement(self):
        return self.arrangement
    
    def save(self,*args, **kwargs):
        super(DialogueGroup, self).save(*args, **kwargs)
        itemAddition("dialogue_group",self.lesson.id,self.id)

    def delete(self,*args, **kwargs):
        itemRomoval("dialogue_group",self.lesson.id,self.id)
        super(DialogueGroup, self).delete(*args, **kwargs)
        
    
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
        DGItemAddition("test_card",self.dialogue_group.id,self.id)
        
    def delete(self,*args, **kwargs):
        print("Inside the class function calledkjdghfidsu gfudsgufdgsgg")
        DGItemRomoval("test_card",self.dialogue_group.id,self.id)
        print("Inside the class function called")
        super(TestCard, self).delete(*args, **kwargs)



TYPE_CHOICES=[
    ('dialogue','dialogue'),
    ('test_card','test_card'),
    ]
class DGItemListMain(models.Model):
    dialogue_group = models.ForeignKey(DialogueGroup, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    item_id = models.PositiveIntegerField(unique=False)
    d_object = models.ForeignKey(Dialogue,on_delete=models.CASCADE,null=True,blank=True)
    tc_object = models.ForeignKey(TestCard,on_delete=models.CASCADE,null=True,blank=True)

    # last_updated = models.DateTimeField(blank=True, editable=False)

    def __str__(self):
        return self.type + ' of id ' + str(self.item_id) + ' in lesson ' + self.dialogue_group.title
    
    
    
    def save(self, *args, **kwargs):
        if(self.type == "dialogue"):
            w = Dialogue.objects.get(id=self.item_id)
            self.d_object = w
        elif(self.type == "test_card"):
            d = TestCard.objects.get(id=self.item_id)
            self.tc_object = d
        super(DGItemListMain,self).save(*args, **kwargs)
        # self.last_updated = timezone.now()
        AddorKeepItem(self.id,self.dialogue_group.id)
        return self.id
    def delete(self, *args, **kwargs):
        RemoveItem(self.id,self.dialogue_group.id)
        super(DGItemListMain,self).delete(*args, **kwargs)
    
def AddorKeepItem(item_id,obj):
    object_ = DialogueGroup.objects.filter(id=obj).first()
    int_array= object_.get_arrangement()
    for id in int_array:
        if item_id == id:
            return
    int_array.append(item_id)
    object_.arrangements = int_array
    object_.save()
    return

def RemoveItem(item_id,obj):
    object_ = DialogueGroup.objects.filter(id=obj).first()
    int_array= object_.get_arrangement()
    index = int_array.index(item_id)
    if index == -1:
        return
    int_array.pop(index)
    object_.arrangements = ",".join(int_array)
    object_.save()  
    return




