from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [path("get-user-id", views.UserDetails.as_view())]
