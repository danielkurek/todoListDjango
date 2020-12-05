from django.shortcuts import render
from django.http import HttpResponse

from .models import ToDoTask

# Create your views here.
def index(request):
    latest_tasks = ToDoTask.objects.order_by('-create_date')[:5]
    output = ', '.join([t.task_title for t in latest_tasks])
    return HttpResponse(output)
def detail(request, task_id):
    return HttpResponse("You're looking at task %s." % task_id)