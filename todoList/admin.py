from django.contrib import admin

from .models import TaskList, ToDoTask, Tag

# Register your models here.
admin.site.register(ToDoTask)
admin.site.register(Tag)
admin.site.register(TaskList)