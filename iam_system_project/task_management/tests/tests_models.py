from django.test import TestCase
from django.utils import timezone
from ..models import Project, Task
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from task_management.models import Project, Task

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email='user@example.com', password='TestPassword123')

    def test_project_creation(self):
        project = Project.objects.create(
            title='Test Project',
            description='Project for testing',
            created_by=self.user,
            date_created=timezone.now()
        )
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'Project for testing')
        self.assertEqual(project.created_by, self.user)
        self.assertIsNotNone(project.date_created)

    def test_project_str_method(self):
        project = Project.objects.create(
            title='Test Project',
            description='Project for testing',
            created_by=self.user,
            date_created=timezone.now()
        )
        self.assertEqual(str(project), 'Test Project')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email='user@example.com', password='TestPassword123')
        self.project = Project.objects.create(
            title='Test Project',
            description='Project for testing',
            created_by=self.user,
            date_created=timezone.now()
        )

    def test_task_creation(self):
        task = Task.objects.create(
        name='Test Task',
        description='Task for testing',
        due_date=timezone.now(),
        completed=False,
        project=self.project,
        status='ready',
        priority='low',
        start_time=timezone.now(),
        end_time=timezone.now(),
        notes='Test notes',
        created_by=self.user
    )
        task.assigned_to.set([self.user])  # Use set method to add users to the many-to-many field
        task.save()

        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.description, 'Task for testing')
        self.assertIsNotNone(task.due_date)
        self.assertFalse(task.completed)
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.assigned_to.first(), self.user)
        self.assertEqual(task.status, 'ready')
        self.assertEqual(task.priority, 'low')
        self.assertIsNotNone(task.start_time)
        self.assertIsNotNone(task.end_time)
        self.assertEqual(task.notes, 'Test notes')
        self.assertEqual(task.created_by, self.user)

    def test_task_str_method(self):
        task = Task.objects.create(
            name='Test Task',
            description='Task for testing',
            due_date=timezone.now(),
            completed=False,
            project=self.project,
            status='ready',
            priority='low',
            start_time=timezone.now(),
            end_time=timezone.now(),
            notes='Test notes',
            created_by=self.user
        )
        task.assigned_to.set([self.user])  # Use set method to add users to the many-to-many field
        task.save()

        self.assertEqual(str(task), 'Test Task')


