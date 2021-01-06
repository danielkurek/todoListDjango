from django.db.models import fields
from django.forms import ModelForm,DateInput
from django.forms import widgets
from django.forms.widgets import DateTimeInput, TextInput

from .models import ToDoTask
from .models import Tag

class DateTimeInput(DateTimeInput):
    input_type = "datetime-local"

class ColorInput(TextInput):
    input_type = "color"

class TaskForm(ModelForm):
    """Form for creating and editing tasks"""
    class Meta:
        model = ToDoTask
        fields = ("task_title", "due_date","task_description", "recurring")
        widgets = {
            "due_date": DateTimeInput,
        }
class TagForm(ModelForm):
    """Form for creating and editing tags"""
    class Meta:
        model = Tag
        fields = ("tag_name", "tag_color")
        widgets = {
            "tag_color": ColorInput
        }
        