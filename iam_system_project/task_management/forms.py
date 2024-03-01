from .models import *
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model  = Project
        fields = ["title","description"]

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ["name","description","priority","status","assigned_to","notes","dependencies","due_date"]
        