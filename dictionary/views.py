from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.viewsets import ViewSet
from .models import Word
from .serializers import *
from django.shortcuts import render
from django.core.files import File
from urllib.parse import unquote

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from dictionary.models import Word
from .models import *
from .serializers import *
from pathlib import Path
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class WordDataUploader(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, id=None):
        wid = request.data.get("id")
        word = Word.objects.filter(id=int(wid)).first()
        print(wid)
        word.meaning = request.data.get("meaning",word.meaning)
        word.subtitle = request.data.get("subtitle",word.subtitle)
        word.category = request.data.get("category",word.category)
        word.pronunciation = request.data.get("pronunciation" ,word.pronunciation)
        word.text = request.data.get("text",word.text)
        word.HSK = request.data.get("HSK",word.HSK)
        word.male_voice = request.data.get("male_voice",word.male_voice)
        word.female_voice = request.data.get("female_voice",word.female_voice)
        word.save()

        serializer = WordSerializer(word)
        return Response(serializer.data)




class HanziActions(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, word=None):
        decoded = unquote(word)
        h_card = Hanzi.objects.filter(word=str(decoded)).first()
        serializer = HanziSerializer(h_card)
        print(serializer.data)
        return Response([serializer.data])        

    def put(self, request, word=None):
        decoded = unquote(word)
        print(decoded)
        hanzi = Hanzi.objects.filter(word=str(decoded)).first()
        if hanzi:
            hanzi.meaning = request.data.get("meaning",hanzi.meaning)
            hanzi.word = request.data.get("word",hanzi.word)
            hanzi.sub_description = request.data.get("sub_description" ,hanzi.sub_description)
            hanzi.description = request.data.get("description",hanzi.description)
            hanzi.subtitle = request.data.get("subtitle",hanzi.subtitle)
            hanzi.hsk = request.data.get("hsk",hanzi.hsk)
            hanzi.strokes_no = request.data.get("strokes_no",hanzi.strokes_no)
            hanzi.video = request.data.get("video",hanzi.video)
            hanzi.image = request.data.get("image",hanzi.image)
            hanzi.save()
            serializer = HanziSerializer(hanzi)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            