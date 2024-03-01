from django.urls import path
from .views import *

urlpatterns = [
    path('',DashboardView.as_view(),name="dashboard"),
    path('create_project', CreateProjectView.as_view(),name="create_project"),
    path('project/<int:pk>/create_task/', CreateTaskView.as_view(),name="create_task"),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='task_detail'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='task_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='task_delete'),

] 