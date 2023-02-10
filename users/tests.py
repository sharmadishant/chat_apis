
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.normal_user = User.objects.create_user(
            username='normal',
            email='normal@example.com',
            password='password'
        )

    def test_admin_user(self):
        self.assertTrue(self.admin_user.is_users)
        self.assertTrue(self.admin_user.is_superuser)

    def test_normal_user(self):
        self.assertFalse(self.normal_user.is_users)
        self.assertFalse(self.normal_user.is_superuser)
