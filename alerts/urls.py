from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("alert-notes-action/",views.NotesActions.as_view()),
    path("alert-popups-action/",views.PopupActions.as_view()),
    path("alert-labels-action/",views.LabelActions.as_view()),
]