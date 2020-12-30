from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import ToDoTask
from .forms import TaskForm

# Create your views here.
def index(request):
    showCompleted = request.GET.get("showCompleted", "")
    if showCompleted == "true":
        showCompleted = True
    else:
        showCompleted = False
       
    tasks = ToDoTask.objects
    if showCompleted == False:
        tasks = tasks.filter(completed=False)
    tasks = tasks.order_by('completed','-create_date')
    
    paginator = Paginator(tasks, 15, orphans=5)
    pageNumber = request.GET.get("page")
    page = paginator.get_page(pageNumber)
    return render(request, 'todoList/taskList.html', 
      {
        'showCompleted': showCompleted,
        'showCompletedParam': "&showCompleted=true" if showCompleted else "",
        'page': page
      })

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