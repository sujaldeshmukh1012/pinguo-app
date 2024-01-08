from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("alert-notes-action/<int:id>/",views.NotesActions.as_view()),
    path("alert-popups-action/<int:id>/",views.PopupActions.as_view()),
    path("alert-labels-action/<int:id>/",views.LabelActions.as_view()),
]