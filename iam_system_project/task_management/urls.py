from django.urls import path
from .views import *

urlpatterns = [
    path('',DashboardView.as_view(),name="dashboard"),   
    path('project_list/',ProjectListView.as_view(),name="project_list"), 
    path('project/create', CreateProjectView.as_view(),name="project_create"), 
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='task_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='task_delete'),
    path('task_list/',TaskListView.as_view(),name="task_list"),
    path('task/create', CreateTaskView.as_view(), name="task_create"),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),    

] 