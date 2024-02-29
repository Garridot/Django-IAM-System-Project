from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser, CustomUserManager, Role, UserRole, AuditLog

class ModelTests(TestCase):

    def setUp(self):
        self.role = Role.objects.create(name='Admin', description='Administrator role')
        self.user_manager = CustomUserManager()

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='user@example.com',
            password='TestPassword123'
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.date_joined.date(), timezone.now().date())
        self.assertFalse(user.roles.exists())  # No roles assigned

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='AdminPassword123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.date_joined.date(), timezone.now().date())
        self.assertFalse(superuser.roles.exists())  # No roles assigned to superuser

    def test_create_role(self):
        role = Role.objects.create(name='Editor', description='Editor role')
        self.assertEqual(role.name, 'Editor')
        self.assertEqual(role.description, 'Editor role')
        self.assertFalse(role.permissions.exists())  # No permissions assigned

    def test_create_user_role(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='TestPassword123')
        user_role = UserRole.objects.create(user=user, role=self.role)
        self.assertEqual(user_role.user, user)
        self.assertEqual(user_role.role, self.role)



    def test_create_audit_log(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='TestPassword123')
        audit_log = AuditLog.objects.create(user=user, action='Login')
        self.assertEqual(audit_log.user, user)
        self.assertEqual(audit_log.action, 'Login')
        self.assertIsNotNone(audit_log.timestamp)

    def test_password_validation(self):
        # Valid password
        self.user_manager.validate_password('ValidPassword123')

        # Invalid password (missing uppercase letter)
        with self.assertRaises(ValidationError):
            self.user_manager.validate_password('invalidpassword123')

    def test_create_user_with_roles(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='TestPassword123')
        role1 = Role.objects.create(name='Role1', description='Role 1')
        role2 = Role.objects.create(name='Role2', description='Role 2')

        # Assign roles to the user
        user.roles.add(role1, role2)

        self.assertEqual(user.roles.count(), 2)
        self.assertTrue(user.roles.filter(name='Role1').exists())
        self.assertTrue(user.roles.filter(name='Role2').exists())

    def test_audit_log_str(self):
        user = CustomUser.objects.create_user(email='user@example.com', password='TestPassword123')
        audit_log = AuditLog.objects.create(user=user, action='Login')

        expected_str = f"{user} - Login - {audit_log.timestamp}"
        self.assertEqual(str(audit_log), expected_str)
