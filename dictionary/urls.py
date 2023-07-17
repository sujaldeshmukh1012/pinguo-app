from django.urls import path, include
from . import views

urlpatterns = [
    path("word-upload/<int:id>/", views.WordDataUploader.as_view()),
]
