from django.forms import ModelForm,DateInput
from django.forms.widgets import DateTimeInput

from .models import ToDoTask

class DateTimeInput(DateTimeInput):
    input_type = "datetime-local"

class TaskForm(ModelForm):
    class Meta:
        model = ToDoTask
        fields = ("task_title", "due_date","task_description")
        widgets = {
            "due_date": DateTimeInput
        }
        