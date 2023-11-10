from django.contrib import admin
from .models import Pinyin,Word,PinyinInitialAndFinal,PinyinTone,ToneNotes,ToneType,Hanzi

# Register your models here.


class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "ideogram", "meaning", "pronunciation", "HSK")
    ordering = ["id"]


admin.site.register(Word, WordAdmin)


class PinyinAdmin(admin.ModelAdmin):
    list_display = ("tone","initial_and_final")
    
    
    
admin.site.register(Pinyin, PinyinAdmin)




class PinyinInitialAndFinalAdmin(admin.ModelAdmin):
    list_display = ("title",)
    
    
    
admin.site.register(PinyinInitialAndFinal, PinyinInitialAndFinalAdmin)


class PinyinToneAdmin(admin.ModelAdmin):
    list_display = ("title",)
    
    
    
admin.site.register(PinyinTone, PinyinToneAdmin)



class ToneNotesAdmin(admin.ModelAdmin):
    list_display = ("tone_text",)
    
    
    
admin.site.register(ToneNotes, ToneNotesAdmin)

class ToneTypeAdmin(admin.ModelAdmin):
    list_display = ("title",
"pinyin_text",
"subheader",
"description",
"female_voice",
"male_voice",)
    
    
    
admin.site.register(ToneType, ToneTypeAdmin)




class HanziAdmin(admin.ModelAdmin):
    list_display = ("word",
"video",
"subtitle",
"meaning",
"image",
"pinyin",
"description",
"sub_description",)
    
    
    
admin.site.register(Hanzi, HanziAdmin)

