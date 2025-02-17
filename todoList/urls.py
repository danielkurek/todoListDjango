from django.urls import path

from . import views

urlpatterns = [
    #list URLs
    path('lists', views.listManage, name='list-manage'),
    path('list/create', views.listCreate, name='list-create'),
    path('list/<int:list_id>/', views.listView, name='list-view'),
    path('list/<int:list_id>/edit', views.listEdit, name='list-edit'),
    path('list/<int:list_id>/delete', views.listDelete, name='list-delete'),
    path('list/deleted', views.listDeleted, name='list-deleted'),

    #task URLs
    path('', views.taskList, name='task-list'),
    path('tasks', views.taskList, name='task-list'),
    path('task/create', views.taskCreate, name='task-create'),
    path('task/<int:task_id>/', views.taskDetail, name='task-detail'),
    path('task/<int:task_id>/complete', views.taskComplete, name='task-complete'),
    path('task/<int:task_id>/edit', views.taskEdit, name='task-edit'),
    path('task/<int:task_id>/delete', views.taskDelete, name='task-delete'),
    path('task/deleted', views.taskDeleted, name='task-deleted'),
    
    #tags URLs
    path('tags', views.tagList, name='tag-list'),
    path('tag/create', views.createTag, name='tag-create'),
    path('tag/<int:tag_id>/edit', views.editTag, name='tag-edit'),
    path('tag/<int:tag_id>/delete', views.deleteTag, name='tag-delete'),
    path('tag/deleted', views.deletedTag, name='tag-deleted'),
]