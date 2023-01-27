from django import forms
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile, Task, Room, Category
from .serializers import ProfileSerializer, TaskListSerializer, TaskDetailSerializer, RoomListSerializer, \
    RoomDetailSerializer, CategorySerializer, UserSerializer
from django.contrib.auth.models import User
from .custompermission import IsCurrentUserProfileOrReadOnly, IsCurrentUser, IsCurrentUserCreatorOrReadOnly
import django_filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet, DateFilter
from django_filters.rest_framework import FilterSet, filters, DateTimeFilter


class ProfileList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'
    filterset_fields = ['nickname']
    search_fields = ['nickname', 'pk']
    ordering_fields = ['nickname']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCurrentUserProfileOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'


class TaskFilter(FilterSet):
    min_start_date = DateFilter(field_name='start_time', lookup_expr='gte', label='Start date from:', widget=forms.DateInput(attrs={'type': 'date'}))
    max_start_date = DateFilter(field_name='start_time', lookup_expr='lte', label='Start date to:', widget=forms.DateInput(attrs={'type': 'date'}))
    min_end_date = DateFilter(field_name='end_time', lookup_expr='gte', label='End date from:', widget=forms.DateInput(attrs={'type': 'date'}))
    max_end_date = DateFilter(field_name='end_time', lookup_expr='lte', label='End date to:', widget=forms.DateInput(attrs={'type': 'date'}))


class TaskList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    name = 'task-list'
    filterset_class = TaskFilter
    filterset_fields = ['description', 'created_by', 'is_important', 'category', 'user_room']
    search_fields = ['description', 'created_by', 'is_important', 'category', 'user_room']
    ordering_fields = ['description', 'start_time', 'end_time']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    name = 'task-detail'


class CategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-detail'


class RoomList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    name = 'room-list'
    filterset_fields = ['name', 'creator', 'category', 'user_room']
    search_fields = ['name', 'creator', 'user_room']
    ordering_fields = ['name', 'pk', 'creator']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        serializer.instance.user_room.add(self.request.user)


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCurrentUserCreatorOrReadOnly]
    name = 'room-detail'
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    filterset_fields = ['username']
    search_fields = ['username']
    ordering_fields = ['username', 'pk']


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCurrentUser]
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
