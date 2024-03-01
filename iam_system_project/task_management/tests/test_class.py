# from django.test import TestCase, Client
# from django.urls import reverse
# from ..forms import ProjectForm, TaskForm
# from ..models import CustomUser, Project, Task

# class TaskManagementTests(TestCase):
#     def setUp(self):
#         # Create a user for testing
#         self.user = CustomUser.objects.create(email='user@example.com', password='TestPassword123')

#         # Create a project for testing
#         self.project = Project.objects.create(title='Test Project', description='Project for testing', created_by=self.user)

#         # Create a task for testing
#         self.task = Task.objects.create(
#             name='Test Task',
#             description='Task for testing',
#             due_date='2022-01-01',
#             project=self.project,
#             created_by=self.user
#         )

#     def test_project_detail_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.get(reverse('project_detail', kwargs={'pk': self.project.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'task_management/task_detail.html')
#         self.assertEqual(response.context['task'], self.project)

#     def test_project_update_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.post(reverse('project_update', kwargs={'pk': self.project.pk}), data={'title': 'Updated Project'})
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
#         self.assertEqual(Project.objects.get(pk=self.project.pk).title, 'Updated Project')

#     def test_project_delete_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.post(reverse('project_delete', kwargs={'pk': self.project.pk}))
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
#         with self.assertRaises(Project.DoesNotExist):
#             Project.objects.get(pk=self.project.pk)

#     def test_create_task_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.get(reverse('create_task', kwargs={'project_id': self.project.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'task_management/task_create.html')

#         response = client.post(reverse('create_task', kwargs={'project_id': self.project.pk}),
#                                data={'name': 'New Task', 'description': 'Task description', 'due_date': '2022-01-01'})
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
#         self.assertTrue(Task.objects.filter(name='New Task').exists())

#     def test_task_detail_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.get(reverse('task_detail', kwargs={'task_id': self.task.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'task_management/task_detail.html')
#         self.assertEqual(response.context['task'], self.task)

#     def test_task_update_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.post(reverse('task_update', kwargs={'pk': self.task.pk}), data={'name': 'Updated Task'})
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
#         self.assertEqual(Task.objects.get(pk=self.task.pk).name, 'Updated Task')

#     def test_task_delete_view(self):
#         client = Client()
#         client.force_login(self.user)

#         response = client.post(reverse('task_delete', kwargs={'pk': self.task.pk}))
#         self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
#         with self.assertRaises(Task.DoesNotExist):
#             Task.objects.get(pk=self.task.pk)
