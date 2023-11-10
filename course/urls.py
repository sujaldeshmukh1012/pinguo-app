from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("courses/", views.CourseList.as_view()),
    path("courses/<int:id>", views.CourseDetail.as_view()),
    path("lessons-details/<int:id>", views.LessonDetail.as_view()),
    path("course-actions/<int:id>/", views.CourseActions.as_view(), name="add-courses"),
    path("lessons/<int:id>", views.LessonList.as_view()),
    # path("lessons-content/<int:id>", views.LessonContent.as_view()),
    path(
        "lessons-actions/<int:id>/", views.LessonActions.as_view(), name="add-courses"
    ),
    path("update/courses/", views.UpdateCourseListIndexing.as_view()),
    path("update/lesson/", views.UpdateLessonListIndexing.as_view()),
    path("lesson-attachments/<int:id>/", views.LessonAllAttachmentsList.as_view()),

    # General Path
    path("lessons-content/<int:id>", views.LessonContent.as_view()),
    
]
