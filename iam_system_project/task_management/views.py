from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from .forms import *
from .models import *

from functools import wraps
from django.http import HttpResponseForbidden

from chat.views import create_chatroom,add_user_chatroom

def user_has_role(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_roles = UserRole.objects.filter(user=request.user)
            
            # Check if the user has any of the allowed roles
            if any(role.name in allowed_roles for user_role in user_roles for role in user_role.role.all()):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to view this page.")
        
        return _wrapped_view

    return decorator

def is_authorized(user,role_selected):
    user_role = UserRole.objects.get(user=user)
    if any(role.name == role_selected for role in user_role.role.all()): 
        return True

class DashboardView(View):    
    template_name = 'task_management/dashboard.html'

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):                      
        tasks = Task.objects.all().order_by('priority', 'due_date')[0:10]
        context = {}  
        context["tasks"] = tasks  

        if is_authorized(request.user,"Admin"): context["is_authorized"] = True 
        else: context["is_authorized"] = False     
        return render(request, self.template_name, context)

class ProjectListView(View):
    template_name = 'task_management/project/projects_list.html'  

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs): 
        projects = Project.objects.all()
        return render(request, self.template_name,{"projects":projects}) 

class CreateProjectView(View):    
    template_name = 'task_management/obj_create.html'   
    form_class  = ProjectForm 
    success_url = reverse_lazy("dashboard")
   
    @method_decorator(login_required, name='dispatch')
    @method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
    def get(self, request, *args, **kwargs):
        form = self.form_class
        obj_name = "Project"
        url_post = reverse_lazy('project_create')
        context = {"form":form,"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context) 

    @method_decorator(login_required, name='dispatch')
    @method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():            
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()        
            create_chatroom(project.title)    
            return HttpResponseRedirect(self.success_url)           

        return render(request, self.template_name, {'form': form})    
               
@method_decorator(login_required, name='dispatch')
class ProjectDetailView(View):
    model = Project
    template_name = 'task_management/project/project_detail.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=int(kwargs.get('pk')))
        context = {"project": project}

        if is_authorized(request.user,"Admin"): context["is_authorized"] = True 
        else: context["is_authorized"] = False   

        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'task_management/obj_update.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):  
        form = self.form_class     
        obj_name = "Project"
        url_post = reverse('project_detail', kwargs={"pk":kwargs.get('pk')})
        context = {"form":form,"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'task_management/obj_delete.html'
    success_url = reverse_lazy('projects_list')

    def get(self, request, *args, **kwargs):       
        obj_name = "Project"
        url_post = reverse_lazy('project_delete',kwargs={"pk":kwargs.get('pk')})
        context = {"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context) 

    def post(self, request, *args, **kwargs):
        obj = int(kwargs.get('pk'))
        Project.objects.get(id=obj).delete()
        return HttpResponseRedirect(self.success_url)

class CreateTaskView(View):    
    template_name = 'task_management/obj_create.html'   
    form_class  = TaskForm 
    success_url = reverse_lazy("dashboard") 
   
    @method_decorator(login_required, name='dispatch')
    @method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        obj_name = "Task"
        url_post = reverse_lazy('task_create')
        context = {"form":form,"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context) 

    @method_decorator(login_required, name='dispatch')
    @method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
    def post(self, request, *args, **kwargs):        

        form = self.form_class(request.POST)
        if form.is_valid():            
            task = form.save(commit=False)            
            task.created_by = request.user            
            task.save()            
            return HttpResponseRedirect(self.success_url)           

        return render(request, self.template_name, {'form': form})    

class TaskListView(View):
    template_name = 'task_management/task/task_list.html'  

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs): 
        tasks = Task.objects.all()
        return render(request, self.template_name,{"tasks":tasks}) 

@method_decorator(login_required, name='dispatch')
class TaskDetailView(View):
    template_name = 'task_management/task/task_detail.html'

    def get(self, request, *args, **kwargs):
        task_id = int(kwargs.get('pk'))
        task = Task.objects.get(id=task_id)
        context = {}
        context["task"] = task
        if is_authorized(request.user,"Admin"): context["is_authorized"] = True 
        else: context["is_authorized"] = False   

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_id = int(kwargs.get('pk'))
        task = Task.objects.get(id=task_id)           
        if request.POST["chose"] == "perform_task":
            task.assigned_to.add(request.user)                        
            task.save()
        elif request.POST["chose"] == "cancel_task":
            task.assigned_to.remove(request.user)
            task.save()

        add_user_chatroom(request.POST["chose"],task,request.user)     

        return render(request, self.template_name, {'task': task})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_management/obj_update.html'
    context_object_name = 'task'

    def get(self, request, *args, **kwargs):  
        form = self.form_class        
        obj_name = "Task"
        url_post = reverse('task_detail', kwargs={"pk":kwargs.get('pk')})
        context = {"form":form,"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_role(['Admin', 'Engineer']), name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_management/obj_delete.html'
    success_url = reverse_lazy('task_list')

    def get(self, request, *args, **kwargs):       
        obj_name = "Task"
        url_post = reverse_lazy('task_delete',kwargs={"pk":kwargs.get('pk')})
        context = {"obj_name":obj_name,"url_post":url_post}
        return render(request, self.template_name, context) 

    def post(self, request, *args, **kwargs):
        obj = int(kwargs.get('pk'))
        Task.objects.get(id=obj).delete()
        return HttpResponseRedirect(self.success_url)

