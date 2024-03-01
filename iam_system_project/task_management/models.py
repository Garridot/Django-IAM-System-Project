from django.db import models
from models.models import *
# Create your models here.


class Project(models.Model):
    title        = models.CharField(max_length=255)
    description  = models.TextField()
    created_by   = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title 


class Task(models.Model):
    STATUS_CHOICES = [
        ('ready', 'Ready to Begin'),
        ('working', 'Working on It'),
        ('waiting', 'Waiting to Review'),
        ('done', 'Done'),
        ('stuck', 'Stuck')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),        
    ]
    
    name        = models.CharField(max_length=255)
    description = models.TextField()
    due_date    = models.DateField(default=timezone.now)
    completed   = models.BooleanField(default=False)
    project     = models.ForeignKey(Project,on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(CustomUser,related_name='assigned_tasks',null=True,blank=True)
    status      = models.CharField(max_length=10,choices=STATUS_CHOICES, default='ready')
    priority    = models.CharField(max_length=10,choices=PRIORITY_CHOICES, default='low')
    start_time  = models.DateTimeField(default=timezone.now,null=True,blank=True)
    end_time    = models.DateTimeField(null=True,blank=True)
    notes = models.TextField(blank=True)    
    dependencies = models.ManyToManyField('self',symmetrical=False, blank=True)
    created_by   = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='created_tasks',default=None)

    def __str__(self):
        return self.name
         