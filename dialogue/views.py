from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import ImageModal,Ballon, Dialogue, DialogueGroup,TestAnswer,TestCard
from .serializers import ImageModalSerializer,BallonSerializer,DialogueGroupSerializer,DialogueSerializer,TestAnswerSerializer,TestCardSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from course.models import Lesson
from django.contrib.auth.models import User
from word_card.models import WordCard
from dictionary.models import Word
from word_card.serializers import WordCardSerializer
from dictionary.serializers import WordSerializer
import string 


# Create your views here.
class DialogueGroupList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        dialogue_grp = DialogueGroup.objects.filter(lesson=id).order_by("-last_updated")
        serializer = DialogueGroupSerializer(dialogue_grp, many=True)
        return Response(serializer.data)


class DialogueGroupActions(APIView):
    def put(self, request, id=None):
        card_Id = request.data.get("card_id")
        dialogue_grp = DialogueGroup.objects.filter(id=card_Id,lesson=id).first()
        serializer = DialogueGroupSerializer(dialogue_grp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):
        dialogue_grp = DialogueGroupSerializer(data=request.data)

        if dialogue_grp.is_valid():
            dialogue_grp.save()
            return Response(dialogue_grp.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        dialogue_grp = DialogueGroup.objects.filter(id=id, user=request.user.id)
        dialogue_grp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DialogueGroupDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        dialoguegrp = DialogueGroup.objects.filter(user=request.user.id, id=id).first()
        serializer = DialogueGroupSerializer(dialoguegrp)
        return Response(serializer.data)


class DialogueList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        dialogue = Dialogue.objects.filter(dialogue_group=id).order_by("-last_updated")
        serializer = DialogueSerializer(dialogue, many=True)
        return Response(serializer.data)


class DialogueActions(APIView):
    def put(self, request, id=None):
        card_Id = request.data.get("card_id")
        dialogue = Dialogue.objects.filter(id=card_Id).first()
        serializer = DialogueSerializer(dialogue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):
        title = request.data.get("title")
        lesson_id = request.data.get("lesson")
        dialogur_grp_id = request.data.get("dialogue_group")
        lesson = Lesson.objects.filter(id=lesson_id)
        dialogue_grp = DialogueGroup.objects.filter(id=dialogur_grp_id)
        dialogue = Dialogue.objects.create(
                    title=title,
                    lesson=lesson.first(),
                    dialogue_group=dialogue_grp.first(),
                    user=request.user,
                )
        dialogue.save()
        serializer = DialogueSerializer(dialogue,many=False)
        return Response(serializer.data)

    def delete(self, request, id=None):
        dialogue = Dialogue.objects.filter(id=id, user=request.user.id)
        dialogue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class DialogueDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        dialoguegrp = Dialogue.objects.filter(user=request.user.id, id=id).first()
        serializer = DialogueSerializer(dialoguegrp)
        return Response(serializer.data)


class ImageModalDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        image = ImageModal.objects.filter(user=request.user.id, id=id).first()
        serializer = ImageModalSerializer(image)
        return Response(serializer.data)


class BallonDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        ballon = Ballon.objects.filter(user=request.user.id, id=id).first()
        serializer = BallonSerializer(ballon)
        return Response(serializer.data)




class ImageModalActions(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ImageModalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BallonActions(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    # serializer = BallonSerializer(data=request.data)
        
    def post(self, request):
        ideogram = request.data.get('ideogram')
        user = request.user
        lesson = request.data.get('lesson')
        spl = ideogram.translate(str.maketrans('', '', string.punctuation)).replace("", " ")
        string_main = listToString(spl)
        pinyin_str_instance = listToString(spl)
        res = [string_main[i: j] for i in range(len(string_main))
          for j in range(i + 1, len(string_main) + 1)]
        ind = len(string_main)
        while ind>=0:    # it will iterate till the index of string_main is not 0
            for i in range(len(res)): # it iterates through the response array
                if len(res[i]) == ind:   # this will make sure i am checking only upper bound substrings
                    get_pin=getPinYin(res[i])# this checks the presence of the substring in the database
                    if get_pin: # if the pinyin is existing

                        if res[i] in pinyin_str_instance:
                            pinyin_str_instance =  pinyin_str_instance.replace(res[i],get_pin+' ')
                        resp_data = CreateLinkedWordCard(res[i],lesson,user.id) 
                        string_main.replace(res[i],"") # this removes the recently found substring from the string_main
            ind=ind-1
            print(pinyin_str_instance)
            #the while loop ends 

        avatar = request.data.get('avatar')
        meaning = request.data.get('meaning')
        file = request.data.get('file')
        ballon = Ballon.objects.create(
                    avatar=avatar,
                    user=request.user, 
                    file=file,
                    ideogram=ideogram,
                    meaning=meaning,  
                    pronunciation=pinyin_str_instance 
                ) 
        ballon.save()
        serializer = BallonSerializer(ballon,many=False)
        return Response(serializer.data)



class TestAnswerActions(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request,id=None):
        text = request.data.get("text")
        test_id = request.data.get("test")
        test = TestCard.objects.filter(id=test_id)
        test_answer_ = TestAnswer.objects.filter(test=test.first(),text=text)
        if test_answer_.exists():
            serializer = TestAnswerSerializer(test_answer_,many=True)
            return Response(serializer.data)
        else:
            test_answer = TestAnswer.objects.create(
                        test=test.first(),
                        user=request.user,
                        text=text
                    )
            test_answer.save()
            serializer = TestAnswerSerializer(test_answer,many=False)
            return Response(serializer.data)
     
    def delete(self, request, id=None):
        test_answer = TestAnswer.objects.filter(id=id, user=request.user.id)
        test_answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TestAnswerDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        test = TestCard.objects.filter(id=id)
        test_answer = TestAnswer.objects.filter(user=request.user.id, test=test.first())
        serializer = TestAnswerSerializer(test_answer,many=True)
        return Response(serializer.data)
 



class TestCardActions(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, id=None):
        dialogue_id = request.data.get("dialogue")
        dialogue_grp_id = request.data.get("dialogue_group")  
        card_type = request.data.get("card_type")
        test_text = request.data.get("test_text")
        dialogue = Dialogue.objects.filter(id=dialogue_id)
        dialogue_grp = DialogueGroup.objects.filter(id=dialogue_grp_id)
        test_card = TestCard.objects.create(
                    dialogue=dialogue.first(),
                    user=request.user,
                    card_type=card_type,
                    dialogue_group=dialogue_grp.first(),
                    test_text=test_text
                )
        test_card.save()
        serializer = TestCardSerializer(test_card,many=False)
        return Response(serializer.data)
    
    def delete(self, request, id=None):
        test_card = TestCard.objects.filter(id=id, user=request.user.id)
        test_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, id=None):
        test_card = TestCard.objects.filter(id=id).first()
        serializer = TestCardSerializer(test_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class TestCardDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        test_card = TestCard.objects.filter(user=request.user.id, id=id).first()
        serializer = TestCardSerializer(test_card)
        return Response(serializer.data)







class DialogueBoxContent(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        grp = DialogueGroup.objects.filter(id=id,user=request.user.id).first()
        dialogue = Dialogue.objects.filter(dialogue_group=grp).order_by('-last_updated')
        dialogue_serializers = DialogueSerializer(dialogue,many=True)
        
        test = TestCard.objects.filter(dialogue_group=grp).order_by('-last_updated')
        test_serializers = TestCardSerializer(test,many=True)
        resp = [dialogue_serializers.data,test_serializers.data]
        return Response(resp)


def CreateLinkedWordCard(word,lessonId,userId):
    print(word,lessonId,userId)
    arr = word.split()
    resp = []
    for i in range(len(arr)):
        type(arr[i])
        lesson = Lesson.objects.filter(id=lessonId)
        user = User.objects.filter(id=userId).first()
        word = Word.objects.filter(ideogram=arr[i])
    if word.exists() and lesson.exists():
        card = WordCard.objects.create(
            word=arr[i],
            lesson=lesson.first(),
            author=user,
            dictionary=word.first(),
            linked=True
        )
        card.save()
        serializer = WordCardSerializer(card)
        resp.append(serializer.data)
    else:
        data = {"status": "error", "error": "Word Does Not Exist"}
        resp.append(data)
    return resp




def getPinYin(word):
    ideo = Word.objects.filter(ideogram=word)
    if ideo.exists():
        return ideo.first().pronunciation
    else:
        return False
    
def detectPunctuations(array):
    punc = [',',":","!",";","?","｡","“","”","•",".","﹑","「","」","『","』"]
    print("entry point array:",array)
    arr=array
    idx=0
    for i in range(len(punc)):
        print("--------")
        if punc[i] in arr:
            idx = arr.index(punc[i])
            # arr.pop(idx,1)
            print("this is the index:",idx)
        else:
            pass
    print("this is the array:",arr)
    return arr




def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1.replace(" ","")
# Driver code