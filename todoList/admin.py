from django.contrib import admin

from .models import ToDoTask, Tag

# Register your models here.
admin.site.register(ToDoTask)
admin.site.register(Tag)