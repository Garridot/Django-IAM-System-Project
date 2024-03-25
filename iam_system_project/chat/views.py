from django.shortcuts import render
from .models import ChatRoom
from task_management.models import *
from django.views import View
from task_management.views import method_decorator,login_required
# Create your views here.

class chatroomsView(View):    
    template_name = 'index.html'

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):                      
        threads = ChatRoom.objects.filter(participants=request.user) 
        context = {"threads": threads}     
        return render(request, self.template_name, context)


def create_chatroom(title):    
    ChatRoom.objects.create(name=title)     
    return True
        
def add_user_chatroom(action,task,user):

    total_tasks = len(Task.objects.filter(project=task.project,assigned_to=user))
    chatroom = ChatRoom.objects.get(name=task.project)

    if action == "perform_task" and total_tasks == 1: 
        chatroom.participants.add(user)
        chatroom.save()

    if action == "cancel_task" and total_tasks == 0: 
        chatroom.participants.remove(user)
        chatroom.save()    

    