from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from .models import ToDoTask, Tag
from .forms import TaskForm, CreateTagForm

# Create your views here.
def index(request):
    showCompleted = request.GET.get("showCompleted", "")
    if showCompleted == "true":
        showCompleted = True
    else:
        showCompleted = False
    
    filterQuery = request.GET.get("q", "")
       
    tasks = ToDoTask.objects
    if showCompleted == False:
        tasks = tasks.filter(completed=False)
    if filterQuery != "":
        tasks = tasks.filter(task_title__icontains=filterQuery)
    tasks = tasks.order_by('completed','-create_date')
    
    paginator = Paginator(tasks, 15, orphans=3)
    pageNumber = request.GET.get("page")
    page = paginator.get_page(pageNumber)
    return render(request, 'todoList/taskList.html', 
      {
        'showCompleted': showCompleted,
        'showCompletedParam': "&showCompleted=true" if showCompleted else "",
        'queryParam': "&q=" + filterQuery if filterQuery != "" else "",
        'page': page
      })

def detail(request, task_id):
    task = ToDoTask.objects.get(id=task_id)
    return render(request, 'todoList/taskDetail.html', {'task': task})

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
            task = form.save()
            tags = request.POST.getlist("tag", [])
            for tagID in tags:
                tag = Tag.objects.get(pk=tagID)
                task.tags.add(tag)
            return redirect("add-task")
    else:
        initalDate = datetime.now() + timedelta(days=1)
        form = TaskForm(
            initial={
                "due_date": initalDate.strftime("%Y-%m-%dT%H:00")
            })
    tags = Tag.objects.order_by("tag_name")
    return render(request, 'todoList/addTask.html', 
        {'form':form, 'urlAction': resolve_url('add-task'), 'tags':tags})

def addTag(request):
    if request.method == "POST":
        form = CreateTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add-tag")
    else:
        form = CreateTagForm(
            initial={
                "tag_color": "#FF0000"
            })
    return render(request, 'todoList/addTask/inputForm.html', 
        {'form':form, 'urlAction': resolve_url('add-tag')})