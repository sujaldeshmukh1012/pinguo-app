from rest_framework import serializers
from .models import *
from dictionary.serializers import *
from rest_framework.serializers import Serializer, FileField


class WordCardSerializer(serializers.ModelSerializer):
    dictionary = WordSerializer(read_only=True)

    class Meta:
        model = WordCard
        fields = "__all__"
