from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/task-list', views.taskList, name='task-list'),
    path('/user-list', views.userList, name='user-list'),
    path('/category-list', views.categoryList, name='category-list'),
    path('/room-list', views.roomList, name='room-list'),
]
