from django.urls import path
from chatting import views, tests

urlpatterns = [
    path('delUser/', views.delUserInGroup, name='rmUser'),
    path('searchUser/', views.searchUserInGroup, name='findUser'),
    path('addUser/', views.addUserInGroup, name='message-message_sendto_db'),
    path('createGroup/', views.createGroup, name='createGroup'),
   
    path('api/messages/update/db', views.message_sendto_db, name='message-message_sendto_db'),
    path('api/messages_view/', views.message_view, name='message-db-view'),
    path('test', tests.APITestCase, name='messagb-view'),
]
