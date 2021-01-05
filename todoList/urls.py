from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-task/', views.input, name='add-task'),
    path('add-tag/', views.addTag, name='add-tag'),
    path('added/', views.added, name='added'),
    path('task/<int:task_id>/', views.detail, name='task-detail'),
    path('task/<int:task_id>/complete', views.complete, name='task-complete'),
    path('task/<int:task_id>/edit', views.editTask, name='task-edit'),
]