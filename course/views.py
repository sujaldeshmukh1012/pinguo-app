from django.shortcuts import render
import json
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Course, Lesson,ItemList
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from word_card.models import WordCard
from word_card.serializers import WordCardSerializer
from dialogue.models import DialogueGroup,Dialogue,TestAnswer,TestCard,Ballon,ImageModal
from dialogue.serializers   import DialogueGroupSerializer
from alerts.models import Note,Popup,Label
from alerts.serializers import NoteSerializer,PopupSerializer,LabelSerializer
from operator import itemgetter
from .duplicateContent import duplicateDialogue,duplicateCourse
import operator
from .objects import syncdata



class CourseList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        status = syncdata()
        print(status)
        courses = Course.objects.filter(author=request.user.id).order_by(
            "-last_updated"
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        courses = Course.objects.filter(author=request.user.id, id=id).first()
        serializer = CourseSerializer(courses)
        return Response(serializer.data)


class LessonDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        lessons = Lesson.objects.filter(author=request.user.id, id=id).first()
        serializer = LessonSerializer(lessons)
        return Response(serializer.data)

class CourseActions(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id=None):
        course = Course.objects.filter(id=id, author=request.user.id).first()
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):
        courses = CourseSerializer(data=request.data)
        old_id = id
        if courses.is_valid():
            courses.save()
            return Response(courses.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        course = Course.objects.filter(id=id, author=request.user.id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseDuplication(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):
        courses = Course.objects.filter(id=id).first()
        old_id = id
        if courses:
            new_course = Course.objects.create(
                title=courses.title,
                author=courses.author,
                info_type=courses.info_type
            )
            new_course.save()
            ser = CourseSerializer(new_course,many=False)
            duplicateCourse(old_id,new_course.id)
            return Response(ser.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DialogueGroupDuplication(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):
        dg = DialogueGroup.objects.filter(id=id).first()
        if dg:
            new_dg = justDiuplicateDialogueGroup(id)
            ser = DialogueGroupSerializer(new_dg,many=False)
            return Response(ser.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
def justDiuplicateDialogueGroup(old_id):
    dg = DialogueGroup.objects.filter(id=old_id).first()
    new_dg = DialogueGroup.objects.create(
            user=dg.user,
            lesson=dg.lesson,
            title=dg.title,
            info_type=dg.info_type
            
        )
    new_dg.save()
    duplicateDialogue(dg,dg.lesson,new_dg)
    return new_dg


class LessonList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        lessons = Lesson.objects.filter(parent_course=id).order_by("-last_updated")
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)





# class LessonContent(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id=None):
#         less = Lesson.objects.filter(id=id,author=request.user.id).first()
#         try:
#             data = less.arragements.get("data",None)
#         except:
#             data = less.arragements
#         if (data == False):
#             # create Data and save()
#             resp = fetchDataAndSave(less)
#             print("Creating Data")
#         else:
#             # fetch data and return
#             resp = GiveResponse(data,less)
#             print("Fetching Data")
#         return Response(resp)


# class LessonContent(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id=None):
#         less = Lesson.objects.filter(id=id,author=request.user.id).first()
#         word_cards = WordCard.objects.filter(lesson=less).order_by('-last_updated')
#         dialogue_grp = DialogueGroup.objects.filter(lesson=less).order_by('-last_updated')
#         notes = Note.objects.filter(lesson=less).order_by('-created')
#         notes_serializer = NoteSerializer(notes, many=True)
#         popups = Popup.objects.filter(lesson=less).order_by('-created')
#         popups_serializer = PopupSerializer(popups, many=True)
        
#         labels = Label.objects.filter(lesson=less).order_by('-created')
#         labels_serializer = LabelSerializer(labels, many=True)
        
#         dia_serializer = DialogueGroupSerializer(dialogue_grp, many=True)
#         w_card__serializer = WordCardSerializer(word_cards, many=True)
#         resp = [w_card__serializer.data,dia_serializer.data,notes_serializer.data,popups_serializer.data,labels_serializer.data]
#         return Response(resp)
    
class LessonContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        lesson = Lesson.objects.filter(id=id).first()
        lists_of_items = ItemList.objects.filter(lesson=lesson)
        data = get_all_data(lists_of_items,lesson.arrangement)
        return data


class LessonAllAttachmentsList(APIView):
        permission_classes = [IsAuthenticated]


        def get(self, request, id=None):
                less = Lesson.objects.filter(id=id,author=request.user.id).first()
                notes = Note.objects.filter(lesson=less).order_by('-created')
                notes_serializer = NoteSerializer(notes, many=True)
                popups = Popup.objects.filter(lesson=less).order_by('-created')
                popups_serializer = PopupSerializer(popups, many=True)
                
                labels = Label.objects.filter(lesson=less).order_by('-created')
                labels_serializer = LabelSerializer(labels, many=True)
                resp = [notes_serializer.data,popups_serializer.data,labels_serializer.data]
                return Response(resp)
# index 0 => notes , index 1 => popups, index 2 => labels 

class ChangeCourseContentList(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,id=None):
        obj = Course.objects.filter(id=id).first()
        item = request.data.get("items")
        obj.arragements =item
        obj.save()
        ser = CourseSerializer(obj,many=False)
        return Response(ser.data)
    
    
class ChangeLessonConetentList(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,id=None):
        obj = Lesson.objects.filter(id=id).first()
        item = request.data.get("items")
        l = []
        for data in item:
            l.append(data.get("item_id",0))
        print(l)
        obj.arrangement =l
        obj.save()
        ser = LessonSerializer(obj,many=False)
        return Response(ser.data)



class LessonActions(APIView):
    def put(self, request, id=None):
        lessons = Lesson.objects.filter(id=id).first()
        serializer = LessonSerializer(lessons, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):
        lessons = LessonSerializer(data=request.data)

        if lessons.is_valid():
            lessons.save()
            return Response(lessons.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        lessons = Lesson.objects.filter(id=id, author=request.user.id)
        lessons.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateCourseListIndexing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data["list"][::-1]
        for i in range(len(data)):
            course = Course.objects.get(id=data[i])
            course.arrangement_number = course.arrangement_number + 1
            course.save()
        courses = Course.objects.filter(author=request.user.id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class UpdateLessonListIndexing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data["list"][::-1]
        for i in range(len(data)):
            lesson = Lesson.objects.get(id=data[i], author=request.user.id)
            lesson.arrangement_number = lesson.arrangement_number + 1
            lesson.save()
        lessons = Lesson.objects.filter(author=request.user.id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

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
    if (type == "word_card"):
        w = WordCard.objects.filter(id=data.item_id).first()
        ser = WordCardSerializer(w,many=False)
        return ser.data
    elif(type=="dialogue_group"):
        w = DialogueGroup.objects.filter(id=data.item_id).first()
        ser = DialogueGroupSerializer(w,many=False)
        return ser.data
    elif(type=="label"):
        w = Label.objects.filter(id=data.item_id).first()
        ser = LabelSerializer(w,many=False)
        return ser.data
    elif(type=="popup"):
        w = Popup.objects.filter(id=data.item_id).first()
        ser = PopupSerializer(w,many=False)
        return ser.data
    elif(type=="note"):
        w = Note.objects.filter(id=data.item_id).first()
        ser = NoteSerializer(w,many=False)
        return ser.data
    