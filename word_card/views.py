from django.shortcuts import render

# Create your views here.
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
from dictionary.models import Word
from .models import *
from .serializers import *
from course.models import Lesson

# Create your views here.


class WordCardOptins(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        data = request.data["words"]
        arr = data.split()
        # here we have an array of seprate operatable words.
        resp = []
        for i in range(len(arr)):
            type(arr[i])
            lesson = Lesson.objects.filter(id=id)
            word = Word.objects.filter(ideogram=arr[i])
            lesson = Lesson.objects.filter(id=id)
            if word.exists() and lesson.exists():
                card = WordCard.objects.create(
                    word=arr[i],
                    lesson=lesson.first(),
                    author=request.user,
                    dictionary=word.first(),
                )
                card.save()
                serializer = WordCardSerializer(card)
                resp.append(serializer.data)
            else:
                data = {"status": "error", "error": "Word Does Not Exist"}
                resp.append(data)
        return Response(resp)

    def put(self, request, id, *args, **kwargs):
        word = request.data["words"]
        card_Id = request.data["card_id"]
        resp = []
        lesson = Lesson.objects.filter(id=id)
        w_card = WordCard.objects.filter(id=card_Id)
        if w_card.exists():
            print("Updating Old=============")
            new_dict = Word.objects.filter(ideogram=word)
            if new_dict.exists():
                card = w_card.first()
                card.word = word
                card.dictionary = new_dict.first()
                card.save()
                serializer = WordCardSerializer(card)
                resp.append(serializer.data)
            else:
                pass
        else:
            print("Creating New.......")
            word = Word.objects.filter(ideogram=data)
            lesson = Lesson.objects.filter(id=id)
            if word.exists() and lesson.exists():
                card = WordCard.objects.create(
                    word=data,
                    lesson=lesson.first(),
                    author=request.user,
                    dictionary=word.first(),
                )
                card.save()
                serializer = WordCardSerializer(card)
                resp.append(serializer.data)
            else:
                data = {"status": "error", "error": "Word Does Not Exist"}
                resp.append(data)
        return Response(resp)

    def delete(self, request, id=None):
        lesson = request.data["lesson"]
        l = Lesson.objects.filter(id=lesson)
        word_card = WordCard.objects.filter(
            id=id, author=request.user.id, lesson=l.first()
        )
        word_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WordCardList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        word_cards = WordCard.objects.filter(
            author=request.user.id, lesson=id
        ).order_by("-last_updated")
        serializer = WordCardSerializer(word_cards, many=True)
        return Response(serializer.data)


class WordCardDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        word_cards = WordCard.objects.filter(author=request.user.id, id=id)
        serializer = WordCardSerializer(word_cards, many=True)
        return Response(serializer.data)


class UpdateWordCardListIndexing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data["list"][::-1]
        for i in range(len(data)):
            word_card = WordCard.objects.get(id=data[i])
            word_card.arrangement_number = word_card.arrangement_number + 1
            word_card.save()
        word_cards = WordCard.objects.filter(author=request.user.id)
        serializer = WordCardSerializer(word_cards, many=True)
        return Response(serializer.data)
