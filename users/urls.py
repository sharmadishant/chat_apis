from django.urls import path
from users import views

urlpatterns = [
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginPage.as_view(), name='login'),
    path('createUser/', views.createUser.as_view(), name='register'),
    path('updateUser/', views.UserUpdateApiView.as_view(), name='update'),
]
