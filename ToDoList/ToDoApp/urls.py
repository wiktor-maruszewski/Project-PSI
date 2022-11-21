from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    # path('/task-list', views.taskList, name='task-list'),
    # path('/user-list', views.ListUsers.as_view(), name='user-list'),
    # path('/category-list', views.categoryList, name='category-list'),
    # path('/room-list', views.roomList, name='room-list'),
    path('TaskList', views.TaskList.as_view(), name='TaskList'),
    path('CategoryList', views.CategoryList.as_view(), name='CategoryList'),
    path('RoomList', views.RoomList.as_view(), name='RoomList'),
    path('UserList', views.UserList.as_view(), name='UserList'),
    path('ProfileList', views.ProfileList.as_view(), name='ProfileList'),
    # path('/UsersRooms', views.UserRoomList.as_view(), name='UsersRooms'),
]
