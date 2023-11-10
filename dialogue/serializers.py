from rest_framework import serializers,fields
from .models import ImageModal,Ballon, Dialogue, DialogueGroup,TestAnswer,TestCard
from course.serializers import LessonSerializer

class ImageModalSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageModal
        fields = "__all__"


class BallonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ballon
        fields = "__all__"


class DialogueGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = DialogueGroup
        fields = "__all__"



class DialogueSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    dialogue_group = DialogueGroupSerializer(read_only=True)
    class Meta:
        model = Dialogue
        fields = "__all__"




class TestCardSerializer(serializers.ModelSerializer):
    dialogue = DialogueSerializer(read_only=True)
    class Meta:
        model = TestCard
        fields = "__all__"



class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = "__all__"
