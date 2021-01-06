from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('task/add', views.input, name='task-add'),
    path('task/<int:task_id>/', views.detail, name='task-detail'),
    path('task/<int:task_id>/complete', views.complete, name='task-complete'),
    path('task/<int:task_id>/edit', views.editTask, name='task-edit'),
    path('task/<int:task_id>/delete', views.deleteTask, name='task-delete'),
    path('task/deleted', views.deletedTask, name='task-deleted'),
    
    path('tags', views.tagList, name='tag-list'),
    path('tag/add', views.addTag, name='tag-add'),
    path('tag/<int:tag_id>/edit', views.editTag, name='tag-edit'),
    path('tag/<int:tag_id>/delete', views.deleteTag, name='tag-delete'),
    path('tag/deleted', views.deletedTag, name='tag-deleted'),
]