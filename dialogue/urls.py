from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # dialogue-group endpoints
    path("dialogue-group/<int:id>", views.DialogueGroupList.as_view()),
    path("dialogue-group-details/<int:id>", views.DialogueGroupDetail.as_view()),
    path("dialogue-group-actions/<int:id>/", views.DialogueGroupActions.as_view(), name="dialogue group actions"),

    #  Image endpoints  
    path("image-details/<int:id>", views.ImageModalDetails.as_view()),
    path("image-actions/", views.ImageModalActions.as_view()),
    
    #  Ballon endpoints  
    path("ballon-details/<int:id>", views.BallonDetails.as_view()),
    path("ballon-actions/", views.BallonActions.as_view()),
    
    # dialogue endpoints
    path("dialogue-details/<int:id>", views.DialogueDetails.as_view(), name="dialogue list"),
    path("dialogue-actions/<int:id>/", views.DialogueActions.as_view(), name="dialogue actions"),
    path("dialogue/<int:id>", views.DialogueList.as_view()),

    # TestAnswer endpoints
    path("testanswer/<int:id>/", views.TestAnswerActions.as_view(), name=""),
    path("testanswer/", views.TestAnswerActions.as_view(), name=""),
    path("testanswer-list/<int:id>", views.TestAnswerDetails.as_view(), name=""),
    
    
        # TestCard endpoints
    path("testcard/", views.TestCardActions.as_view(), name=""),
    path("testcard/<int:id>/", views.TestCardActions.as_view(), name=""),
    path("testcard-details/<int:id>", views.TestCardDetails.as_view(), name=""),
    
    # General Paths
    path("dialogue-grp/<int:id>", views.DialogueBoxContent.as_view(), name=""),
]
