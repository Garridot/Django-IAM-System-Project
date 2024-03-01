from django.contrib import admin
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'date_created')
    list_filter = ('created_by', 'date_created')
    search_fields = ('title', 'description')

admin.site.register(Project, ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date', 'completed', 'status', 'priority')
    list_filter = ('project', 'assigned_to', 'status', 'priority', 'completed')
    search_fields = ('name', 'description')
    date_hierarchy = 'due_date'
    ordering = ('due_date',)

admin.site.register(Task, TaskAdmin)

