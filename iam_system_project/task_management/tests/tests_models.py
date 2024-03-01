from django.test import TestCase
from django.utils import timezone
from ..models import CustomUser, Project, Task

class TaskManagementModelTests(TestCase):
    def setUp(self):
        # Create a custom user for testing
        self.user = CustomUser.objects.create(email='user@example.com', password='TestPassword123')

        # Create a project for testing
        self.project = Project.objects.create(
            title='Test Project',
            description='This is a test project',
            created_by=self.user,
            date_created=timezone.now()
        )

    def test_project_str(self):
        # Test the __str__ method of the Project model
        self.assertEqual(str(self.project), 'Test Project')

    def test_task_str(self):
        # Create a task for testing
        task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            due_date=timezone.now().date(),
            completed=False,
            project=self.project
        )

        # Test the __str__ method of the Task model
        self.assertEqual(str(task), 'Test Task')

    def test_task_defaults(self):
        # Test default values of a new task
        task = Task.objects.create(name='Default Task', due_date=timezone.now().date(), project=self.project)
        self.assertFalse(task.completed)
        self.assertEqual(task.status, 'ready')
        self.assertEqual(task.priority, 'low')
        self.assertIsNone(task.start_time)
        self.assertIsNone(task.end_time)
        self.assertEqual(task.notes, '')
        self.assertEqual(task.dependencies.count(), 0)

    def test_task_dependencies(self):
        # Create two tasks and add one as a dependency to the other
        task1 = Task.objects.create(name='Task 1', due_date=timezone.now().date(), project=self.project)
        task2 = Task.objects.create(name='Task 2', due_date=timezone.now().date(), project=self.project)
        task2.dependencies.add(task1)

        # Test if task2 has task1 as a dependency
        self.assertEqual(task2.dependencies.count(), 1)
        self.assertIn(task1, task2.dependencies.all())
