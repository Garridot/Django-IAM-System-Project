from django.shortcuts import render
from .models import ChatRoom
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



