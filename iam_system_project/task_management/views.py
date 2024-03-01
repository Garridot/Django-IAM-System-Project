from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from .forms import *
from .models import *


class DashboardView(View):    
    template_name = 'task_management/dashboard.html'

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):                      
        tasks = Task.objects.all().order_by('priority', 'due_date')[0:10]
        context = {}  
        context["task"] = tasks         
        return render(request, self.template_name, context)

class ProjectListView(View):
    template_name = 'task_management/projects_list.html'  

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs): 
        projects = Project.objects.all()
        return render(request, self.template_name,projects) 

class TaskListView(View):
    template_name = 'task_management/task_list.html'  

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs): 
        tasks = Task.objects.all()
        return render(request, self.template_name,tasks) 

class CreateProjectView(View):    
    template_name = 'task_management/create_project.html'   
    form_class  = ProjectForm 
    success_url = reverse_lazy("dashboard")
   
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form}) 

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():            
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return HttpResponseRedirect(self.success_url)           

        return render(request, self.template_name, {'form': form})    
               
@method_decorator(login_required, name='dispatch')
class ProjectDetailView(View):
    model = Project
    template_name = 'task_management/project_detail.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=int(kwargs.get('pk')))
        context = {"project": project}
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'task_management/project_update.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'task_management/project_delete.html'
    success_url = reverse_lazy('dashboard')

class CreateTaskView(View):    
    template_name = 'task_management/task_create.html'   
    form_class  = TaskForm 
    success_url = reverse_lazy("dashboard") 
   
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):

        form = self.form_class()
        project_id = int(kwargs.get('pk'))  
        context = {'form': form,"project_id":project_id}       
        return render(request, self.template_name,context) 

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):

        project_id = int(kwargs.get('pk'))  

        form = self.form_class(request.POST)
        if form.is_valid():            
            task = form.save(commit=False)
            task.project    = Project.objects.get(id=project_id)
            task.created_by = request.user            
            task.save()
            return HttpResponseRedirect(self.success_url)           

        return render(request, self.template_name, {'form': form})    

@method_decorator(login_required, name='dispatch')
class TaskDetailView(View):
    template_name = 'task_management/task_detail.html'

    def get(self, request, *args, **kwargs):
        task_id = int(kwargs.get('pk'))
        task = Task.objects.get(id=task_id)
        return render(request, self.template_name, {'task': task})

    def post(self, request, *args, **kwargs):
        task_id = int(kwargs.get('pk'))
        task = Task.objects.get(id=task_id)

        if request.POST.get("perform_task"):
            task.assigned_to.add(request.user)
            task.save()
        elif request.POST.get("cancel_task"):
            task.assigned_to.remove(request.user)
            task.save()

        return render(request, self.template_name, {'task': task})

@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_management/task_update.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_management/task_delete.html'
    success_url = reverse_lazy('dashboard')

