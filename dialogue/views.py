from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import ImageModal,Ballon, Dialogue, DialogueGroup,TestAnswer,TestCard,DGItemListMain
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
from .data import *
from operator import itemgetter
import operator
from course.duplicateContent import duplicateBallon,duplicateImage,duplicateTestAnswers




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
    
class ChangeDialogueList(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,id=None):
        obj = DialogueGroup.objects.filter(id=id).first()
        item = request.data.get("items")
        l = []
        for data in item:
            l.append(data.get("item_id",0))
        obj.arrangement = l
        obj.save()
        ser = DialogueGroupSerializer(obj,many=False)
        return Response(ser.data)

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
        pinyin_str_instance= ReturnPunctuations(ideogram,lesson,user)
        ideogram = ideogram.replace("。","")

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

    def put(self, request):
        ideogram = request.data.get('ideogram')
        id = request.data.get('id')
        user = request.user
        lesson = request.data.get('lesson')
        pinyin_str_instance= ReturnPunctuations(ideogram,lesson,user)
        avatar = request.data.get('avatar')
        meaning = request.data.get('meaning')
        file = request.data.get('file')
        ballon =  Ballon.objects.filter(id=id).first()
        ballon.ideogram = ideogram or ballon.ideogram
        ballon.avatar = avatar or ballon.avatar
        ballon.pronunciation = pinyin_str_instance
        ballon.meaning = meaning or ballon.meaning 
        ballon.file = file or ballon.file
        ballon.save()
        serializer = BallonSerializer(ballon,many=False)
        return Response(serializer.data)


def ReturnPunctuations(ideogram,lesson,user):
    spl = ideogram.translate(str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")).replace("", " ")
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
    return pinyin_str_instance

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
 
class DialogueDuplication(APIView):
    permission_classes = [IsAuthenticated]


    def post(self,request,id=None):
        old_d = Dialogue.objects.filter(id=id).first()
        new_d = Dialogue.objects.create(
        user=old_d.user,
        lesson=old_d.lesson,
        dialogue_group=old_d.dialogue_group,
        title=old_d.title,
        )
        all_ballons= old_d.ballon.all()
        all_image = old_d.image.all()
        for i in all_ballons:
            new_id = duplicateBallon(i.id)
            new_d.ballon.add(new_id)
        for j in all_image:
            new_i_id = duplicateImage(j.id)
            new_d.image.add(new_i_id)
        new_d.save()
        ser = DialogueSerializer(new_d,many=False)
        return Response(ser.data) 
class DuplicateTestCard(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,id=None):
        old_test = TestCard.objects.filter(id=id).first()
        new_test = TestCard.objects.create(
            dialogue_group=old_test.dialogue_group,
            dialogue=old_test.dialogue,
            card_type=old_test.card_type,
            user=old_test.user,
            test_text=old_test.test_text,
            hide=old_test.hide
        )
        new_test.save()
        new_answers = duplicateTestAnswers(old_test,new_test)
        for answer in new_answers:
            new_test.answers.add(answer)
        new_test.save()
        ser = TestCardSerializer(new_test,many=False)
        return Response(ser.data)

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
        print(id,"Its getting deleted")
        test_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, id=None):
        test_card = TestCard.objects.filter(id=id).first()
        serializer = TestCardSerializer(test_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddSelectedBallonToDialogue(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, _id=None,id_=None):
        test_card = TestCard.objects.filter(id=_id).first()
        ballon = Ballon.objects.filter(id=id_)
        test_card.edited_ballon= ballon.first()
        test_card.save()
        serializer = TestCardSerializer(test_card,many=False)
        return Response(serializer.data)
    
    
class TestCardDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        test_card = TestCard.objects.filter(user=request.user.id, id=id).first()
        serializer = TestCardSerializer(test_card)
        return Response(serializer.data)







class DialogueBoxContent(APIView):
    permission_classes = [IsAuthenticated]
 
 
    def get(self, request, id=None):
        dg = DialogueGroup.objects.filter(id=id).first()
        lists_of_items = DGItemListMain.objects.filter(dialogue_group=dg)
        data = get_all_data(lists_of_items,dg.arrangement)
        return data
    # def get(self, request, id=None):
    #     al_d = Dialogue.objects.all()
    #     for d in al_d:
    #         d.save()
    #     al_test = TestCard.objects.all()
    #     for t in al_test:
    #         t.save()
    #     return Response({"message":"true"})
    
    
    
    
    
def CreateLinkedWordCard(word,lessonId,userId):

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
    punc = [',',":","!",";","?","｡","“","”","•",".","﹑","「","」","『","』","。"]

    arr=array
    idx=0
    for i in range(len(punc)):

        if punc[i] in arr:
            idx = arr.index(punc[i])
            # arr.pop(idx,1)

        else:
            pass

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




def getObjectsFromUrl(url):
    # sample = "/dialogue-group/23"
    data = url.lstrip("/").rstrip("/").split("/")
    #sample = ["dialogue-group","23"]
    st = ""
    inti = ""
    for item in data:
        if (item.isdigit()):
            inti = int(item)
        else:
            st = item
    if st== "dialogue-group":
        data = getDialogue_group(inti)

    elif st == "dialogue":
        data = getDialogue_list(inti)
        # data = DialogueGroup.objects.filter(id=inti).first()
    return data

def getAllData(grp):
        test = TestCard.objects.filter(dialogue_group=grp).order_by('-last_updated')
        dialogue = Dialogue.objects.filter(dialogue_group=grp).order_by('-last_updated')
        main_data = [test,dialogue]
        items=[]
        for item in main_data:
            for data in item:
                d={}
                d['id'] = data.id
                d['info_type'] = data.info_type
                d["created"] = data.created.timestamp()
                items.append(d)
        newlist = sorted(items, key=itemgetter('created'), reverse=True)
        return newlist

def fetchDataAndSave(grp):
        newlist = getAllData(grp)
        grp.arragements = newlist
        grp.save()
        res = GiveResponse(newlist,grp)
        return res
def GiveResponse(NewList,grp):
    all_data = getAllData(grp)
    data_to_add = []
    data_to_remove=[]
    for i in all_data:
        if (i not in NewList):
            data_to_add.append(i)

    for k in NewList:
        if (k not in all_data):
            data_to_remove.append(k)
    # remove first
    for rem_data in NewList:
        if (rem_data in data_to_remove):
            ind = NewList.index(rem_data)
            NewList.pop(ind)

    # add later
    for adddata in data_to_add:
        NewList.insert(0,adddata)

    grp.arragements = NewList
    grp.save()
    
    main_data =[]
    for data in NewList:
        if data["info_type"] == "dialogue":
            d= Dialogue.objects.filter(id=data['id']).first()
            d_s = DialogueSerializer(d,many=False)
            main_data.append(d_s.data)
        if data["info_type"] == "test_card":
            p= TestCard.objects.filter(id=data['id']).first()
            p_s = TestCardSerializer(p,many=False)
            main_data.append(p_s.data)
    return main_data





def get_all_data(list_of_items,arrangement):
    data = []    
    # Create a mapping of IDs to their desired positions
    id_to_position = {id: index for index, id in enumerate(arrangement)}
    # Sort list_of_items based on the object.id's position in the id_to_position mapping
    sorted_items = sorted(list_of_items, key=operator.attrgetter("id"), reverse=True)  # Reverse for descending order
    sorted_items.sort(key=lambda item: id_to_position[item.id])
    for obj in sorted_items:
        ret = serialize_this_item(obj)
        ret['item_id'] = obj.id
        data.append(ret)
    # Now sorted_items will be in the same order as the arrangement list
    return Response(data)



def serialize_this_item(data):
    type = data.type
    if (type == "dialogue"):
        w = Dialogue.objects.filter(id=data.item_id).first()
        ser = DialogueSerializer(w,many=False)
        return ser.data
    elif(type=="test_card"):
        w = TestCard.objects.filter(id=data.item_id).first()
        ser = TestCardSerializer(w,many=False)
        return ser.data