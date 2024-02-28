from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Role, UserRole
from django.core.exceptions import ValidationError

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='Passw@rd123',
            # Add any additional fields as needed
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('Passw@rd123'))
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='Adminpassw@rd123',
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password('Adminpassw@rd123'))

    def test_password_validation(self):
        User = get_user_model()

        # Test password with less than 10 characters
        with self.assertRaises(ValidationError) as cm:
            User.objects.create_user(email='test1@example.com', password='pass123')
        self.assertIn('at least 10 characters', str(cm.exception))

        # Test password without numbers
        with self.assertRaises(ValidationError) as cm:
            User.objects.create_user(email='test2@example.com', password='password!')
        self.assertIn('This password is too short. It must contain at least 10 characters.', str(cm.exception))

        # Test password without special characters
        with self.assertRaises(ValidationError) as cm:
            User.objects.create_user(email='test3@example.com', password='Password123')
        self.assertIn('This password is too common.', str(cm.exception))

        # Test password without uppercase letters
        with self.assertRaises(ValidationError) as cm:
            User.objects.create_user(email='test4@example.com', password='passw@rd123')
        self.assertIn('Password must contain at least one uppercase letter.', str(cm.exception))
       

# class RoleModelTest(TestCase):
#     def test_create_role(self):
#         role = Role.objects.create(
#             name='TestRole',
#             description='Test role description',
#         )
#         self.assertEqual(role.name, 'TestRole')
#         self.assertEqual(role.description, 'Test role description')

# class UserRoleModelTest(TestCase):
#     def test_create_user_role(self):
#         User = get_user_model()
#         user = User.objects.create_user(
#             email='user@example.com',
#             password='userpassword123',
#         )
#         role = Role.objects.create(
#             name='TestRole',
#             description='Test role description',
#         )
#         user_role = UserRole.objects.create(
#             user=user,
#             role=role,
#         )
#         self.assertEqual(user_role.user, user)
#         self.assertEqual(user_role.role, role)

#     def test_user_role_str_representation(self):
#         User = get_user_model()
#         user = User.objects.create_user(
#             email='user@example.com',
#             password='userpassword123',
#         )
#         role = Role.objects.create(
#             name='TestRole',
#             description='Test role description',
#         )
#         user_role = UserRole.objects.create(
#             user=user,
#             role=role,
#         )
#         expected_str = f"{user} - {role}"
#         self.assertEqual(str(user_role), expected_str)

