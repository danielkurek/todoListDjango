from django.shortcuts import redirect, render
from django.urls import reverse
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
    filterTags = request.GET.getlist("tags")
    filterDate = request.GET.get("date", "")
       
    tasks = ToDoTask.objects
    title = ""
    if filterDate != "":
        date = datetime.now()
        if filterDate == "today":
            title = "Today"
            tasks = tasks.filter(due_date__lte=date.strftime("%Y-%m-%d"))
        if filterDate == "week":
            title = "This week"
            tasks = tasks.filter(
                due_date__lte=(date+timedelta(weeks=1)).strftime("%Y-%m-%d"))
    if showCompleted == False:
        tasks = tasks.filter(completed=False)
    if filterQuery != "":
        tasks = tasks.filter(task_title__icontains=filterQuery)
    if len(filterTags) > 0:
        for i in range(len(filterTags)):
            # remove non integer values
            try:
                filterTags[i] = int(filterTags[i])
            except ValueError:
                filterTags.remove(i)
                continue
            tasks = tasks.filter(tags__pk=filterTags[i])
    tasks = tasks.order_by('completed','due_date')
    
    paginator = Paginator(tasks, 15, orphans=3)
    pageNumber = request.GET.get("page")
    page = paginator.get_page(pageNumber)
    
    tags = Tag.objects.order_by('tag_name')

    return render(request, 'todoList/taskList.html', 
      {
        'titleText': title,
        'showCompleted': showCompleted,
        'showCompletedParam': "&showCompleted=true" if showCompleted else "",
        'queryParam': "&q=" + filterQuery if filterQuery != "" else "",
        'page': page,
        'tags': tags,
        'selectedTags': filterTags,
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
    if task.recurring != ToDoTask.Recurring.ONCE and task.created_next == False:
        newDate:datetime = task.due_date
        if task.recurring == ToDoTask.Recurring.DAILY:
            newDate += timedelta(days=1)
        elif task.recurring == ToDoTask.Recurring.WEEKLY:
            newDate += timedelta(weeks=1)
        elif task.recurring == ToDoTask.Recurring.MONTHLY:
            newDate += timedelta(weeks=4)
        elif task.recurring == ToDoTask.Recurring.YEARLY:
            newDate += timedelta(days=365)
        newTask = ToDoTask(
            task_title = task.task_title,
            due_date = newDate,
            task_description = task.task_description,
            recurring = task.recurring
            )
        newTask.save()
        for tag in task.tags.all():
            newTask.tags.add(tag)
        task.created_next = True
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
            tagIDs = request.POST.getlist("tag", [])
            tags = []
            for tagID in tagIDs:
                tag = Tag.objects.get(pk=tagID)
                tags.append(tag)
            task.tags.set(tags)
            return redirect("add-task")
    else:
        initalDate = datetime.now() + timedelta(days=1)
        form = TaskForm(
            initial={
                "due_date": initalDate.strftime("%Y-%m-%dT%H:00")
            })
    tags = Tag.objects.order_by("tag_name")
    return render(request, 'todoList/forms/taskForm.html', 
        {'form':form, 'urlAction': reverse('add-task'), 'tags':tags})

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
    return render(request, 'todoList/forms/inputForm.html', 
        {'form':form, 'urlAction': reverse('add-tag')})

def editTask(request, task_id):
    try:
        task = ToDoTask.objects.get(pk=task_id)
    except ToDoTask.DoesNotExist:
        return HttpResponse("Task not found.")
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            tagIDs = request.POST.getlist("tag", [])
            tags = []
            for tagID in tagIDs:
                tag = Tag.objects.get(pk=tagID)
                tags.append(tag)
            task.tags.set(tags)
            return redirect("task-detail", task_id=task_id)
    else:
        form = TaskForm(instance=task, 
            initial={
                "due_date": task.due_date.strftime("%Y-%m-%dT%H:%M")
            }
        )
    tags = Tag.objects.order_by("tag_name")
    task_tags = []
    for tag in task.tags.all():
        task_tags.append(tag.pk)
    return render(request, 'todoList/forms/taskForm.html', 
        {
            'form': form, 
            'urlAction': reverse('task-edit', args=[task_id]),
            'tags': tags,
            'taskTags': task_tags,
        })
def deleted(request):
    return render(request, 'todoList/message.html', 
        {
            'message_text': 'Task has been deleted',
            'url': reverse('index'),
            'button_text': 'Return Home',
        })
def deleteTask(request, task_id):
    try:
        task = ToDoTask.objects.get(pk=task_id)
    except ToDoTask.DoesNotExist:
        return HttpResponse("Task not found.")
    if request.method == "POST":
        if request.POST.get("delete", "false") == "true":
            task.delete()
            return redirect('task-deleted')
    
    return render(request, 'todoList/forms/delete.html', 
        {
            'item': task.task_title,
            'keep_url': reverse('task-detail', args=[task_id]),
            'delete_url': reverse('task-delete', args=[task_id])
        })