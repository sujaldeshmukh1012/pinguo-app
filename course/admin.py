from django.contrib import admin
from .models import *


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "date_added")
    ordering = ["-last_updated"]


admin.site.register(Course, CourseAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "date_added")
    ordering = ["-last_updated"]


admin.site.register(Lesson, LessonAdmin)


class ItemListAdmin(admin.ModelAdmin):
    list_display = ("id","type","item_id","lesson")
    # ordering = ["-last_updated"]
    
    
admin.site.register(ItemList, ItemListAdmin)