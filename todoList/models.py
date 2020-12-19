from django.db import models

# Create your models here.
class ToDoTask(models.Model):
    task_title = models.CharField(max_length=255)
    create_date = models.DateTimeField('date created', auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    task_description = models.TextField(blank=True)
    completed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.task_title

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_color = models.CharField(max_length=9) # color as #AARRGGBB

class TaskTags(models.Model):
    task = models.ForeignKey(ToDoTask, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)