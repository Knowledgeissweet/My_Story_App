from django.contrib import admin
from .models import Category, Story

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display=['title','publish']
    search_fields=['title',]

# Register your models here.
