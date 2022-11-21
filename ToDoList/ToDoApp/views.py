from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ToDoApp.models import Task, Room, Category, Profile, UserRoom
from ToDoApp.serializers import TaskSerializer, RoomSerializer, CategorySerializer, ProfileSerializer, \
    UserRoomSerializer, UserSerializer
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("<center><h1>Our first page</h1></center>")


class TaskList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        permission_classes = [IsAdminUser]
        data = {
            'id': request.data.get('id'),
            'name': request.data.get('name'),
            'creator_id': request.data.get('creator_id')
                }

        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, format=None):
        users = User.objects.all()
        return Response(users.values())

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = RoomSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoomList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserRoomSerializer
    queryset = UserRoom.objects.all()

    def get(self, request, format=None):
        usersrooms = UserRoom.objects.all()
        serializer = RoomSerializer(usersrooms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        userroom = request.data.get('UserRoom')
        serializer = UserRoomSerializer(data=userroom)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
