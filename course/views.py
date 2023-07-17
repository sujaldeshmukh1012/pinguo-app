from django.shortcuts import render

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
        if courses.is_valid():
            courses.save()
            return Response(courses.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        course = Course.objects.filter(id=id, author=request.user.id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        lessons = Lesson.objects.filter(parent_course=id).order_by("-last_updated")
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


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
