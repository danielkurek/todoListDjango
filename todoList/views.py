from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import ToDoTask
from .forms import TaskForm

# Create your views here.
def index(request):
    tasks = ToDoTask.objects.order_by('completed','-create_date')[:5]
    return render(request, 'todoList/taskList.html', {'tasks':tasks})

def detail(request, task_id):
    return HttpResponse("You're looking at task %s." % task_id)

def complete(request, task_id):
    complete = True
    if request.method == "GET":
        complete = request.GET.get("complete", "")
        if complete == "false":
            complete = False
        else:
            complete = True
    task = ToDoTask.objects.get(id=task_id)
    task.completed = complete
    task.save()
    # return HttpResponse("Task completed" if complete else "Task uncompleted")
    return redirect("index")
        

def added(request):
    return HttpResponse("Task has been added")

def input(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add-task")
    else:
        form = TaskForm()
    return render(request, 'todoList/addTask/inputForm.html', {'form':form})