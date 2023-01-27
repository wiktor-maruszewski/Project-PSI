from django.urls import path
from . import views

urlpatterns = [
    path('users', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('profiles', views.ProfileList.as_view(), name=views.ProfileList.name),
    path('profiles/<int:pk>', views.ProfileDetail.as_view(), name=views.ProfileDetail.name),
    path('rooms', views.RoomList.as_view(), name=views.RoomList.name),
    path('rooms/<int:pk>', views.RoomDetail.as_view(), name=views.RoomDetail.name),
    path('categories', views.CategoryList.as_view(), name=views.CategoryList.name),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name=views.CategoryDetail.name),
    path('tasks', views.TaskList.as_view(), name=views.TaskList.name),
    path('tasks/<int:pk>', views.TaskDetail.as_view(), name=views.TaskDetail.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    ]
