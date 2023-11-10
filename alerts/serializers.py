from rest_framework import serializers,fields
from .models import Popup,Label,Note



class PopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = "__all__"
        
        
        
        


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
        
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"