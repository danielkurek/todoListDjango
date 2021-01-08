from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from .models import TaskList, ToDoTask, Tag
from .forms import ListForm, TaskForm, TagForm


def taskList(request, list_id=None):
    """Render index page"""
    
    title = "Tasks" #title of page

    #Get parameters from URL
    showCompleted = request.GET.get("showCompleted", "")
    if showCompleted == "true":
        showCompleted = True
    else:
        showCompleted = False
    
    filterQuery = request.GET.get("q", "")
    filterTags = request.GET.getlist("tags")
    filterDate = request.GET.get("date", "")
    
    #Get tasks from database
    tasks = ToDoTask.objects

    if list_id != None:
        try:
            taskList = TaskList.objects.get(pk=list_id)
        except TaskList.DoesNotExist:
            return HttpResponse("Task list not found")
        tasks = tasks.filter(task_list_id=list_id)
        title = taskList.list_name
    
    #filter tasks with parameters from URL
    if filterDate != "":
        date = datetime.now()
        if filterDate == "today":
            #show only tasks due today or tasks that are past their due date
            title = "Today"
            tasks = tasks.filter(due_date__lte=date.strftime("%Y-%m-%d"))

        if filterDate == "week":
            #show only tasks whose due date is less than date in one week
            title = "This week"
            tasks = tasks.filter(
                due_date__lte=(date+timedelta(weeks=1)).strftime("%Y-%m-%d"))
    
    if showCompleted == False:  #show only uncompleted tasks
        tasks = tasks.filter(completed=False)

    if filterQuery != "":  #filter by task title
        tasks = tasks.filter(task_title__icontains=filterQuery)
    
    if len(filterTags) > 0:  #show tasks with all tags that were selected
        for i in range(len(filterTags)):
            # remove non integer values
            try:
                filterTags[i] = int(filterTags[i])
            except ValueError:
                filterTags.remove(i)
                continue
            
            tasks = tasks.filter(tags__pk=filterTags[i])
    #Sort tasks, show uncompleted tasks with oldest due date first
    tasks = tasks.order_by('completed','due_date')
    
    #Create pages, each page has 15 items,
    #if last page has 3 or less items, display them in previous page
    paginator = Paginator(tasks, 15, orphans=3)
    pageNumber = request.GET.get("page")
    page = paginator.get_page(pageNumber)
    
    #Get all tags to enable user to filter by them
    tags = Tag.objects.order_by('tag_name')

    #Get first 5 task lists to show them in sidebar
    # taskLists = TaskList.objects.all().order_by('list_name')[:5]

    return render(request, 'todoList/taskList.html', 
      {
        'titleText': title,
        'showCompleted': showCompleted,
        'showCompletedParam': "&showCompleted=true" if showCompleted else "",
        'queryParam': "&q=" + filterQuery if filterQuery != "" else "",
        'page': page,
        'tags': tags,
        'selectedTags': filterTags,
        # 'taskLists': taskLists,
      })

def taskDetail(request, task_id):
    """Render page with task details"""
    task = ToDoTask.objects.get(id=task_id)
    return render(request, 'todoList/taskDetail.html', {'task': task})

def taskComplete(request, task_id):
    """Complete or uncomplete task"""
    
    # get parameters from URL
    complete = request.GET.get("complete", "")
    if complete == "false":
        complete = False
    else:
        complete = True
    
    # get task and (un)complete it
    task = ToDoTask.objects.get(id=task_id)
    task.completed = complete
    task.save()
    
    # create next recurring task
    if task.recurring != ToDoTask.Recurring.ONCE and task.created_next == False:
        # determine next due date of recurring task
        newDate:datetime = task.due_date
        if task.recurring == ToDoTask.Recurring.DAILY:
            newDate += timedelta(days=1)
        elif task.recurring == ToDoTask.Recurring.WEEKLY:
            newDate += timedelta(weeks=1)
        elif task.recurring == ToDoTask.Recurring.MONTHLY:
            newDate += timedelta(weeks=4)
        elif task.recurring == ToDoTask.Recurring.YEARLY:
            newDate += timedelta(days=365)
        
        # create new task with same informations and new due date
        newTask = ToDoTask(
            task_title = task.task_title,
            due_date = newDate,
            task_description = task.task_description,
            recurring = task.recurring
            )
        newTask.save()

        # add tags to new task
        newTask.tags.set(list(task.tags.all()))

        # save that next recurring task was created
        # (to avoid duplicates)
        task.created_next = True
        task.save()
    
    return redirect("task-list")

def taskCreate(request):
    """Render form to create task and process it"""
    
    if request.method == "POST":
        # process data and save it
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # add tags to task
            tagIDs = request.POST.getlist("tag", [])
            tags = []
            for tagID in tagIDs:
                tag = Tag.objects.get(pk=tagID)
                tags.append(tag)
            task.tags.set(tags)

            return redirect("task-create")
    else:
        # create form with initial date
        initalDate = datetime.now() + timedelta(days=1)
        form = TaskForm(
            initial={
                "due_date": initalDate.strftime("%Y-%m-%dT%H:00")
            })
    
    # get tags to display them in form
    tags = Tag.objects.order_by("tag_name")

    return render(request, 'todoList/forms/taskForm.html', 
        {
            'form':form, 
            'urlAction': reverse('task-create'), 
            'tags':tags,
        })

def taskEdit(request, task_id):
    """Render form to edit task and process it"""
    
    # get task or show error message
    try:
        task = ToDoTask.objects.get(pk=task_id)
    except ToDoTask.DoesNotExist:
        return HttpResponse("Task not found.")
    
    # process data from form
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            
            # update tags
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
    
    # get tags to display them in form
    tags = Tag.objects.order_by("tag_name")
    
    # get tags that are assigned to task being editted
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

def taskDeleted(request):
    """Render message of task being deleted successfully"""

    return render(request, 'todoList/message.html', 
        {
            'message_text': 'Task has been deleted',
            'url': reverse('task-list'),
            'button_text': 'Return Home',
        })
def taskDelete(request, task_id):
    """Render delete confirmation and process answer - deletion of task"""
    
    # get task or display error if it does not exist
    try:
        task = ToDoTask.objects.get(pk=task_id)
    except ToDoTask.DoesNotExist:
        return HttpResponse("Task not found.")
    
    # process answer on form
    if request.method == "POST":

        # deletion of task
        if request.POST.get("delete", "false") == "true":
            task.delete()
            return redirect('task-deleted')
    
    # render confirmation form
    return render(request, 'todoList/forms/delete.html', 
        {
            'item': task.task_title,
            'keep_url': reverse('task-detail', args=[task_id]),
            'delete_url': reverse('task-delete', args=[task_id])
        })
    
def tagList(request):
    """Render list of all tags"""

    tags = Tag.objects.all()
    return render(request, 'todoList/tagList.html', {'tags':tags})

def createTag(request):
    """Render form for creation of tag and process it"""

    # process submitted form
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tag-create")
    else:
        # create form with initial color
        form = TagForm(
            initial={
                "tag_color": "#FF0000"
            })
    
    return render(request, 'todoList/forms/inputForm.html', 
        {
            'form':form,
            'urlAction': reverse('tag-create'),
            'titleText': 'Add Tag',
        })

def editTag(request, tag_id):
    """Render form for editing tag and process it"""

    # get tag or diplay error if it does not exist
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist:
        return HttpResponse("Tag not found.")
    
    # process submitted form
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("tag-list")
    else:
        # create new form
        form = TagForm(instance=tag)
    
    return render(request, 'todoList/forms/inputForm.html', 
        {
            'form': form,
            'urlAction': reverse('tag-edit', args=[tag_id]),
            'titleText': 'Edit Tag',
        })

def deleteTag(request, tag_id):
    """Render delete confirmation of tag and process answer - deletion of tag"""
    
    # get tag or display message if it does not exist
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist:
        return HttpResponse("Task not found.")
    
    # process answer
    if request.method == "POST":
        # delete tag
        if request.POST.get("delete", "false") == "true":
            tag.delete()
            return redirect('tag-deleted')
    
    return render(request, 'todoList/forms/delete.html', 
        {
            'item': tag.tag_name,
            'keep_url': reverse('tag-list'),
            'delete_url': reverse('tag-delete', args=[tag_id])
        })

def deletedTag(request):
    """Render message after successfully deleting tag"""

    return render(request, 'todoList/message.html', 
        {
            'message_text': 'Tag has been deleted',
            'url': reverse('tag-list'),
            'button_text': 'Return Home',
        })

def listManage(request):
    taskLists = TaskList.objects.all()

    return render(request, 'todoList/listManage.html',{'taskLists': taskLists})

def listCreate(request):
    """Render form for creation of list and process it"""
    
    # process submitted form
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            newList = form.save()
            return redirect("list-view", list_id=newList.id)
    else:
        form = ListForm()
    
    return render(request, 'todoList/forms/inputForm.html', 
        {
            'form': form,
            'urlAction': reverse('list-create'),
            'titleText': 'Create List',
        })

def listView(request, list_id):
    return taskList(request, list_id)

def listEdit(request, list_id):
    """Render form for creation of list and process it"""

    # get list or display message if it does not exist
    try:
        taskList = TaskList.objects.get(pk=list_id)
    except Tag.DoesNotExist:
        return HttpResponse("List not found.")
    
    # process submitted form
    if request.method == "POST":
        form = ListForm(request.POST, instance=taskList)
        if form.is_valid():
            form.save()
            return redirect("list-view", list_id=list_id)
    else:
        form = ListForm(instance=taskList)
    
    return render(request, 'todoList/forms/inputForm.html', 
        {
            'form': form,
            'urlAction': reverse('list-edit'),
            'titleText': f'Edit {taskList.list_name}',
        })

def listDelete(request, list_id):
    """Render delete confirmation of list and process it
     (delete list and all of its tasks)"""
    
    # get list or display message if it does not exist
    try:
        taskList = TaskList.objects.get(pk=list_id)
    except Tag.DoesNotExist:
        return HttpResponse("List not found.")
    
    # process answer
    if request.method == "POST":
        # delete tag
        if request.POST.get("delete", "false") == "true":
            taskList.delete()
            return redirect('list-deleted')
    
    return render(request, 'todoList/forms/delete.html', 
        {
            'item': taskList.tag_name,
            'keep_url': reverse('list-view', args=[list_id]),
            'delete_url': reverse('list-delete', args=[list_id])
        })

def listDeleted(request):
    """Render message after successfully deleting tag"""

    return render(request, 'todoList/message.html', 
        {
            'message_text': 'List has been deleted',
            'url': reverse('task-list'),
            'button_text': 'Return Home',
        })