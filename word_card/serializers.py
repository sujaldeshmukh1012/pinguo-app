from rest_framework import serializers
from .models import *
from dictionary.serializers import *
from rest_framework.serializers import Serializer, FileField
from alerts.serializers import PopupSerializer,LabelSerializer,NoteSerializer

class WordCardSerializer(serializers.ModelSerializer):
    dictionary = WordSerializer(read_only=True)
    # popup_linked = PopupSerializer(read_only=False)
    # note_linked = NoteSerializer(read_only=False)
    # label_linked = LabelSerializer(read_only=False)
    class Meta:
        model = WordCard
        fields = "__all__"

