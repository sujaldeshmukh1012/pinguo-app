from django.contrib import admin
from .models import ImageModal, Ballon , Dialogue , DialogueGroup,TestAnswer,TestCard
# Register your models here.



class ImageModalAdmin(admin.ModelAdmin):
    list_display = ("id", "hints", "file","user")
    ordering = ["-last_updated"]


admin.site.register(ImageModal, ImageModalAdmin)


class BallonAdmin(admin.ModelAdmin):
    list_display = ("id", "ideogram","meaning", "file","avatar")
    ordering = ["-last_updated"]


admin.site.register(Ballon, BallonAdmin)


class DialogueAdmin(admin.ModelAdmin):
    list_display = ("id", "title","lesson","dialogue_group")
    ordering = ["-last_updated"]


admin.site.register(Dialogue, DialogueAdmin)




class DialogueGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "title","lesson")
    ordering = ["-last_updated"]


admin.site.register(DialogueGroup, DialogueGroupAdmin)



class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "text","test","user")
    ordering = ["-last_updated"]


admin.site.register(TestAnswer, TestAnswerAdmin)


class TestCardAdmin(admin.ModelAdmin):
    list_display = ("id", "test_text",'card_type',"dialogue","user")
    ordering = ["-last_updated"]


admin.site.register(TestCard, TestCardAdmin)
