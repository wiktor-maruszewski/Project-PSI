from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from .models import Profile, Task, Room, Category
from .serializers import ProfileSerializer, TaskListSerializer, TaskDetailSerializer, RoomListSerializer, RoomDetailSerializer, CategorySerializer, UserSerializer
from django.contrib.auth.models import User


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    name = 'task-list'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    name = 'task-detail'


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    name = 'room-list'

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        serializer.instance.user_room.add(self.request.user)


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'room-detail'
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'categories': reverse(CategoryList.name, request=request),
                         'tasks': reverse(TaskList.name, request=request),
                         'profiles': reverse(ProfileList.name, request=request),
                         'rooms': reverse(RoomList.name, request=request),
                         'users': reverse(UserList.name, request=request)
                         })
