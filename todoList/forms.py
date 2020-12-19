from django.forms import ModelForm,DateInput

from .models import ToDoTask

class DateInput(DateInput):
    input_type = "date"

class TaskForm(ModelForm):
    class Meta:
        model = ToDoTask
        fields = ("task_title", "due_date","task_description")
        widgets = {
            "due_date": DateInput()
        }
        