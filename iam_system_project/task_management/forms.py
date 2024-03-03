from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model  = Project
        fields = ["title","description"]

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ["name","description","project","priority","status","due_date"]
        