from word_card.models import WordCard
from dialogue.models import DialogueGroup,Dialogue,TestCard
from alerts.models import Label,Popup,Note


def giveMeObject(type,object_id):
        if(type == "word_card"):
            w = WordCard.objects.get(id=object_id)
            return w
        elif(type == "dialogue_group"):
            d = DialogueGroup.objects.get(id=object_id)
            return d
        elif(type == "label"):
            l = Label.objects.get(id=object_id)
            return l
        elif(type == "note"):
            n = Note.objects.get(id=object_id)
            return n
        elif(type == "popup"):
            p = Popup.objects.get(id=object_id)
            return p
        else:
            return None
        
        
def syncdata():
    try:
            
        w =WordCard.objects.all()
        d =Dialogue.objects.all()
        dg =DialogueGroup.objects.all()
        l =Label.objects.all()
        p =Popup.objects.all()
        t =TestCard.objects.all()
        n =Note.objects.all()
        data = [w,d,dg,l,p,t,n]
        for obj in data:
            for item in obj:
                item.save()
        
        return True 
    except:
        return False