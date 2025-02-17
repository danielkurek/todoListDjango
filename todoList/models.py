from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Tag(models.Model):
    
    tag_name = models.CharField(max_length=50)
    tag_color = models.CharField(max_length=7) # color #RRGGBB

    def __str__(self):
        return f"{self.tag_name} - {self.tag_color}"

class TaskList(models.Model):
    list_name = models.CharField(max_length=255)
    create_date = models.DateTimeField('date created', auto_now_add=True)
    
    def __str__(self):
        return self.list_name
class ToDoTask(models.Model):

    class Recurring(models.TextChoices):
        ONCE = "OC", _("Once")
        DAILY = "DY", _("Daily")
        WEEKLY = "WK", _("Weekly")
        MONTHLY = "MN", _("Monthly")
        YEARLY = "YR", _("Yearly")
    
    task_title = models.CharField(max_length=255)
    create_date = models.DateTimeField('date created', auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    task_description = models.TextField(blank=True)
    completed = models.BooleanField(default=False, blank=True)
    tags = models.ManyToManyField(Tag)
    recurring = models.CharField(
        max_length=2, 
        choices=Recurring.choices,
        default=Recurring.ONCE,
    )
    created_next = models.BooleanField(default=False)

    task_list = models.ForeignKey(TaskList, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_title
    
    @property
    def is_past_due(self):
        return self.due_date < timezone.now()
