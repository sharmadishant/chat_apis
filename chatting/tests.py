from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework import status
import time

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='test@example.com',
            email='test@example.com',
            password='12345'
        )
        self.normal_user = User.objects.create_user(
            username='normal@example.com',
            email='normal@example.com',
            password='12345'
        )

        token = self.client.post('/users/login/', {
            'username': 'normal@example.com',
            'email': 'normal@example.com',
            'password': '12345'
        })
        token = f'Bearer {token.data["token"]}'
        self.headers_normanUser = {'HTTP_AUTHORIZATION' : token, 'content_type':'application/json'}
        
        token = self.client.post('/users/login/', {
            'username': 'test@example.com',
            'email': 'test@example.com',
            'password': '12345'
        })
        token = f'Bearer {token.data["token"]}'
        self.headers_superuser = {'HTTP_AUTHORIZATION' : token, 'content_type':'application/json'}
        
        # Test logout
        # response = self.client.post('/logout/')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_admin_login(self):
        response_login = self.client.post('/users/login/', {
            'username': 'normal@example.com',
            'email': 'normal@example.com',
            'password': '12345'
        })
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        time.sleep(1)
        response = self.client.patch('/users/updateUser/',  {
            'username': 'test_normal@example.com'   
        }, **self.headers_normanUser )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # self.assertEqual(User.objects.get(pk=2).email, 'test2@example.com')

    # def test_room_management(self):
    #     # Login as normal user
    #     self.client.login(username='normal', password='password')

    #     # Test creating a group
    #     response = self.client.post('/room/', {
    #         'name': 'group1'
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Test searching for groups
    #     response = self.client.get('/room/?search=group1')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    #     # Test adding members to a group
    #     response = self.client.post('/groups/1/add_members/', {
    #         'members': [2]
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Test deleting a group
    #     response = self.client.delete('/groups/1/')
    #     self.assertEqual(response.status_code,)
    

    # def test_login_logout(self):
        # Test login
        # response = self.client.post('/login/', {
        #     'username': 'normal',
        #     'password': 'password'
        # })
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
      
        # Test creating a group
        response = self.client.post('/users/createGroup/', {
            'room_name': 'sagar '
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test searching for groups
        response = self.client.post('/users/searchUser/?search=all',{
            "room_id":4 
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test adding members to a group
        response = self.client.post('/groups/1/add_members/', {
            "room_id": 4 ,
            "username":" test_normal@example.com"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test deleting a group
        response = self.client.delete('/groups/1/')
        self.assertEqual(response.status_code,)