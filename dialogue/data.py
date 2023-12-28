from .models import *
from .serializers import *

def getDialogue_group(id=None):
    dialogue_grp = DialogueGroup.objects.filter(lesson=id).order_by("-last_updated")
    return dialogue_grp

def getDialogue_list(id=None):
    dialogue = Dialogue.objects.filter(dialogue_group=id).order_by("-last_updated")
    return dialogue

