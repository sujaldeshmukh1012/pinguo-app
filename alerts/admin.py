from django.contrib import admin
from .models import Note,Popup,Label
# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "file","subtitle","text","created")
    ordering = ["-created"]


admin.site.register(Note, NoteAdmin)



class PopupAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "file","text","created")
    ordering = ["-created"]


admin.site.register(Popup, PopupAdmin)


class LabelAdmin(admin.ModelAdmin):
    list_display = ("id", "title","created")
    ordering = ["-created"]


admin.site.register(Label, LabelAdmin)
