from django.urls import path, include
from . import views

urlpatterns = [
    path("wordcard-options/<int:id>/", views.WordCardOptins.as_view()),
    path("wordcard-update/<int:id>/", views.WordCardUpdate.as_view()),
    path("wordcard/<int:id>", views.WordCardList.as_view()),
    path("wordcard-details/<int:id>", views.WordCardDetails.as_view()),
    path("update/wordcards/", views.UpdateWordCardListIndexing.as_view()),
]
