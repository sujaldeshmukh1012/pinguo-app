from django.contrib import admin
from .models import *

# Register your models here.


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "ideogram", "meaning", "pronunciation", "HSK")
    ordering = ["id"]


admin.site.register(Word, WordAdmin)
