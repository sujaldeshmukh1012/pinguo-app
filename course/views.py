from django.shortcuts import render
import json
# Create your views here.
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Course, Lesson
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

class CourseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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


class LessonContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        less = Lesson.objects.filter(id=id,author=request.user.id).first()
        word_cards = WordCard.objects.filter(lesson=less).order_by('-last_updated')
        dialogue_grp = DialogueGroup.objects.filter(lesson=less).order_by('-last_updated')
        notes = Note.objects.filter(lesson=less).order_by('-created')
        notes_serializer = NoteSerializer(notes, many=True)
        popups = Popup.objects.filter(lesson=less).order_by('-created')
        popups_serializer = PopupSerializer(popups, many=True)
        
        labels = Label.objects.filter(lesson=less).order_by('-created')
        labels_serializer = LabelSerializer(labels, many=True)
        
        dia_serializer = DialogueGroupSerializer(dialogue_grp, many=True)
        w_card__serializer = WordCardSerializer(word_cards, many=True)
        resp = [w_card__serializer.data,dia_serializer.data,notes_serializer.data,popups_serializer.data,labels_serializer.data]
        return Response(resp)




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
        print(item)
        obj.arragements =item
        obj.save()
        ser = CourseSerializer(obj,many=False)
        return Response(ser.data)
    
    
class ChangeLessonConetentList(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,id=None):
        obj = Lesson.objects.filter(id=id).first()
        item = request.data.get("items")
        print(item)
        obj.arragements =item
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


def duplicateCourse(old_id,new_id):
    # step 1 : retrieve all stuffs related to course with old_id and
    # then store their id's and model names in a linked list.
    course = Course.objects.filter(id=old_id).first()
    duplicateLessons(new_id,course)
    #  step 2 : take the linked list and duplicate everything with same level
    #  of depth and save new id's in a same type linked list.
    return True

def duplicateLessons(new_id,course_object):
    all_lessons = Lesson.objects.filter(parent_course=course_object)
    new_course = Course.objects.filter(id=new_id).first()
    for object_ in all_lessons:
        new_lesson = Lesson.objects.create(
            parent_course=new_course,
            title=object_.title,
            author=object_.author,
            info_type=object_.info_type
        )
        new_lesson.save()
        duplicateDialogueGrp(object_,new_lesson)
        duplicateWordCards(object_,new_lesson)
    return True



def duplicateWordCards(o_l,n_l):
    all_Word_cards = WordCard.objects.filter(lesson=o_l)
    for wc in all_Word_cards:
        new_WC = WordCard.objects.create(
            word=wc.word,
            author=wc.author,
            dictionary=wc.dictionary,
            lesson=n_l,
            linked=wc.linked,
            info_type=wc.info_type
            # popup_linked=
            # note_linked
            # label_linked
        )
        new_WC.save()
        new_popups = duplicate_popups(o_l,n_l)
        for pop in new_popups:
            new_WC.popup_linked.add(pop)
            
        new_note_linked = duplicate_note_linked(o_l,n_l)
        for pop in new_note_linked:
            new_WC.note_linked.add(pop)
        new_label = duplicate_label(o_l,n_l)
        for nl in new_label:
            new_WC.label_linked.add(nl)
        new_WC.save()
    return True
def duplicate_popups(ol,nl):
    out=[]
    all_p = Popup.objects.filter(lesson=ol)
    for p in all_p:
        new_p = Popup.objects.create(
            title=p.title,
            file=p.file,
            text=p.text,
            lesson=nl,
            info_type=p.info_type
        )
        new_p.save()
        out.append(new_p.id)
    return out
def duplicate_note_linked(ol,nl):
    all_nl = Note.objects.filter(lesson=ol)
    out=[]
    for p in all_nl:
        new_p = Note.objects.create(
            title=p.title,
            file=p.file,
            text=p.text,
            lesson=nl,
            info_type=p.info_type,
            subtitle=p.subtitle
        )
        new_p.save()
        out.append(new_p.id)

    return out
def duplicate_label(ol,nl):
    out=[]
    all_nl = Label.objects.filter(lesson=ol)
    for p in all_nl:
        new_p = Label.objects.create(
            title=p.title,
            lesson=nl,
            info_type=p.info_type,
        )
        new_p.save()
        out.append(new_p.id)
    return out


def duplicateDialogueGrp(old_object,new_object):
    all_dg = DialogueGroup.objects.filter(lesson=old_object)
    for object_ in all_dg:
        new_dg = DialogueGroup.objects.create(
            user=object_.user,
            lesson=new_object,
            title=object_.title,
            info_type=object_.info_type
        )
        new_dg.save()
        duplicateDialogue(object_,new_object,new_dg)
    return True

def duplicateDialogue(old_dg,new_lesson,new_dg):
    all_d = Dialogue.objects.filter(dialogue_group=old_dg,)
    for object_ in all_d:
        new_d = Dialogue.objects.create(
        user=object_.user,
        lesson=new_lesson,
        dialogue_group=new_dg,
        title=object_.title,
        )
        all_ballons= object_.ballon.all()
        all_image = object_.image.all()
        for i in all_ballons:
            new_id = duplicateBallon(i.id)
            new_d.ballon.add(new_id)
        for j in all_image:
            new_i_id = duplicateImage(j.id)
            new_d.image.add(new_i_id)
        new_d.save()
        all_tests = TestCard.objects.filter(dialogue=object_)
        for test in all_tests:
            new_test = TestCard.objects.create(
                dialogue_group=new_dg,
                dialogue=new_d,
                card_type=test.card_type,
                user=test.user,
                test_text=test.test_text,
                hide=test.hide
            )
            new_test.save()
            new_answers = duplicateTestAnswers(test,new_test)
            for answer in new_answers:
                new_test.answers.add(answer)
            new_test.save()
    return True

def duplicateTestAnswers(old,new):
    all_answers = TestAnswer.objects.filter(test=old)
    out=[]
    for answer in all_answers:
        new_a = TestAnswer.objects.create(
            text=answer.text,
            test=new,
            answer_type=answer.answer_type,
            user=answer.user,
            info_type=answer.info_type
        )
        new_a.save()
        out.append(new_a.id)
    return out
def duplicateBallon(i):
    ob = Ballon.objects.filter(id=i).first()
    new_bal = Ballon.objects.create(
        avatar=ob.avatar,
        file=ob.file,
        meaning=ob.meaning,
        ideogram=ob.ideogram,
        pronunciation=ob.pronunciation,
        user=ob.user,
        info_type=ob.info_type
    )
    new_bal.save()
    return new_bal.id
def duplicateImage(i):
    ob = ImageModal.objects.filter(id=i).first()
    new_img = ImageModal.objects.create(
        file=ob.file,
        user=ob.user,
        info_type=ob.info_type,
        hints=ob.hints
    )
    new_img.save()
    return new_img.id


# def getAllData(less):
#         word_cards = WordCard.objects.filter(lesson=less).order_by('-created')
#         dialogue_grp = DialogueGroup.objects.filter(lesson=less).order_by('-created')
#         notes = Note.objects.filter(lesson=less).order_by('-created')
#         popups = Popup.objects.filter(lesson=less).order_by('-created')
#         labels = Label.objects.filter(lesson=less).order_by('-created')
#         main_data = [word_cards,dialogue_grp,notes,popups,labels]
#         items=[]
#         for item in main_data:
#             for data in item:
#                 d={}
#                 d['id'] = data.id
#                 d['info_type'] = data.info_type
#                 d["created"] = data.created.timestamp()
#                 items.append(d)
#         newlist = sorted(items, key=itemgetter('created'), reverse=True)
#         return newlist

# def fetchDataAndSave(less):
#         newlist = getAllData(less)
#         less.arragements = newlist
#         less.save()
#         res = GiveResponse(newlist,less)
#         return res

# def GiveResponse(NewList,less):
#     all_data = getAllData(less)
#     data_to_add = []
#     data_to_remove=[]
#     for i in range(len(all_data)):
#         if (all_data[i] not in NewList):
#             data_to_add.append(all_data[i])

#     for k in range(len(NewList)):
#         if (NewList[k] not in all_data):
#             data_to_remove.append(NewList[k])
#     print(data_to_add)
#     # remove first
#     for rem_data in NewList:
#         if (rem_data in data_to_remove):
#             ind = NewList.index(rem_data)
#             NewList.pop(ind)
#             print(NewList)
#     # add later
#     for adddata in data_to_add:
#         NewList.insert(0,adddata)
#     print(data_to_remove)
#     less.arragements = NewList
#     less.save()
#     main_data =[]
#     for data in NewList:
#         if data['info_type'] == "word_card":
#             w= WordCard.objects.filter(id=data['id']).first()
#             w_s = WordCardSerializer(w,many=False)
#             main_data.append(w_s.data)
#         if data["info_type"] == "dialogue_group":
#             d= DialogueGroup.objects.filter(id=data['id']).first()
#             d_s = DialogueGroupSerializer(d,many=False)
#             main_data.append(d_s.data)
#         if data["info_type"] == "popup":
#             p= Popup.objects.filter(id=data['id']).first()
#             p_s = PopupSerializer(p,many=False)
#             main_data.append(p_s.data)
#         if data["info_type"] == "label":
#             l= Label.objects.filter(id=data['id']).first()
#             l_s = LabelSerializer(l,many=False)
#             main_data.append(l_s.data)
#         if data["info_type"] == "note":
#             n= Note.objects.filter(id=data['id']).first()
#             n_s = NoteSerializer(n,many=False)
#             main_data.append(n_s.data)
#     return main_data

