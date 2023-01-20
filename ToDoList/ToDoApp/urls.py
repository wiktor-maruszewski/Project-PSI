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
    path('TaskList', views.TaskList.as_view(), name=views.TaskList.name),
    path('TaskList/<int:pk>', views.SpecificTask.as_view(), name=views.SpecificTask.name),

    path('CategoryList', views.CategoryList.as_view(), name=views.CategoryList.name),
    path('CategoryList/<int:pk>', views.SpecificCategory.as_view(), name=views.SpecificCategory.name),

    path('RoomList', views.RoomList.as_view(), name=views.RoomList.name),
    path('RoomList/<int:pk>', views.SpecificRoom.as_view(), name=views.SpecificRoom.name),

    path('UserList/', views.UserList.as_view(), name='UserList'),
    # path('SpecificUser/<int:pk>', views.SpecificUser.as_view(), name='UserList'),

    path('ProfileList', views.ProfileList.as_view(), name=views.ProfileList.name),
    path('ProfileList/<int:pk>', views.SpecificProfile.as_view(), name=views.SpecificProfile.name),

    path('UserRoomList', views.UserRoomList.as_view(), name=views.UserRoomList.name),
    path('UserRoomList/<int:pk>', views.SpecificUserRoom.as_view(), name=views.SpecificUserRoom.name),
]
