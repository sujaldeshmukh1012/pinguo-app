from django.shortcuts import render
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import Popup,Note,Label
from .serializers import PopupSerializer,NoteSerializer,LabelSerializer
from course.models import Lesson
# Create your views here.
class NotesActions(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) 
    
    def post(self,request,id=None):
        
        title = request.data.get('title')
        subtitle = request.data.get('subtitle')
        file = request.data.get('file')
        lesson = request.data.get('lesson')
        find_lesson = Lesson.objects.filter(id=lesson).first()
        text = request.data.get('text')
        notes = Note.objects.create(
            title=title,
            subtitle=subtitle,
            file=file,
            text=text,
            lesson=find_lesson
        )
        notes.save()
        serializers = NoteSerializer(notes,many=False)
        return Response(serializers.data)
    
    def put(self, request, id=None):
        instance = Note.objects.filter(id=id).first()
        serializer = NoteSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None):
        notes = Note.objects.filter(id=id)
        notes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
class PopupActions(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self,request,id=None):
        
        title = request.data.get('title')
        file = request.data.get('file')
        lesson = request.data.get('lesson')
        find_lesson = Lesson.objects.filter(id=lesson).first()
        text = request.data.get('text')
        popups = Popup.objects.create(
            title=title,
            file=file,
            text=text,
            lesson=find_lesson
        )
        popups.save()
        serializers = PopupSerializer(popups,many=False)
        return Response(serializers.data)
    
    def put(self, request, id=None):
        instance = Popup.objects.filter(id=id).first()
        serializer = PopupSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id=None):
        popups = Popup.objects.filter(id=id)
        popups.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
class LabelActions(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self,request,id=None):
        title = request.data.get('title')
        lesson = request.data.get('lesson')
        find_lesson = Lesson.objects.filter(id=lesson).first()
        labels = Label.objects.create(
            title=title,
            lesson=find_lesson
        )
        labels.save()
        serializers = LabelSerializer(labels,many=False)
        return Response(serializers.data)
    def put(self, request, id=None):
        instance = Label.objects.filter(id=id).first()
        serializer = LabelSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id=None):
        labels = Label.objects.filter(id=id)
        labels.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)