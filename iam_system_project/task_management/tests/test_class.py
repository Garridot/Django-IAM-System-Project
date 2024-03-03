from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, Task
from ..forms import *

class ProjectTaskManagementTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(email= 'testuser@example.com',password= 'Testp@ssword123',  )

        # Create a test project
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Project Description',
            created_by=self.user  # Set the created_by field
        )

        # Create a test task
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            priority='High',
            status='Not Started',
            project=self.project,
            created_by=self.user,
        )


    def test_project_detail_view(self):
        # Login the user
        self.client.login(email= 'testuser@example.com',password= 'Testp@ssword123')
        # Access the project detail view
        response = self.client.get(reverse('project_detail', kwargs={'pk': self.project.pk}))
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check that the project is present in the contexts
        self.assertEqual(response.context['project'], self.project)

    def test_create_task_view(self):
        # Login the user
        self.client.login(email= 'testuser@example.com',password= 'Testp@ssword123')
        # Access the create task view
        response = self.client.get(reverse('task_create'))
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check that the form is present in the context
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_detail_view(self):
        # Login the user
        self.client.login(email= 'testuser@example.com',password= 'Testp@ssword123')

        # Access the task detail view
        response = self.client.get(reverse('task_detail', kwargs={'pk': self.task.pk}))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the task is present in the context
        self.assertEqual(response.context['task'], self.task)

    def tearDown(self):
        # Clean up any created objects
        self.user.delete()
        self.project.delete()
        self.task.delete()
