from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.viewsets import ViewSet
from .models import Word
from .serializers import *
from django.shortcuts import render
from django.core.files import File

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
        word = Word.objects.filter(id=id).first()
        serializer = WordSerializer(word, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
