from rest_framework import serializers
from .models import *


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = "__all__"

class HanziSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hanzi
        fields="__all__"