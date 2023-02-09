from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework import status

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_login_logout(self):
        # Test login
        response = self.client.post('/login/', {
            'username': 'normal',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        # Test logout
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_management(self):
        # Login as admin
        self.client.login(username='admin', password='password')

        # Test creating a user (only accessible by admin)
        response = self.client.post('/users/', {
            'username': 'newuser',
            'email': 'mailto:newuser@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test editing a user (only accessible by admin)
        response = self.client.patch('/users/2/', {
            'email': 'mailto:newuser2@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=2).email, 'mailto:newuser2@example.com')

    def test_group_management(self):
        # Login as normal user
        self.client.login(username='normal', password='password')

        # Test creating a group
        response = self.client.post('/groups/', {
            'name': 'group1'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test searching for groups
        response = self.client.get('/groups/?search=group1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test adding members to a group
        response = self.client.post('/groups/1/add_members/', {
            'members': [2]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test deleting a group
        response = self.client.delete('/groups/1/')
        self.assertEqual(response.status_code,)
