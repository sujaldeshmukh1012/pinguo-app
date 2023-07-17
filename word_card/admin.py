from django.contrib import admin
from .models import *


# Register your models here.
class WordCardAdmin(admin.ModelAdmin):
    list_display = ("id", "word", "author")
    ordering = ["-last_updated"]


admin.site.register(WordCard, WordCardAdmin)
