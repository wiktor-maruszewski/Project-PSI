from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=30, blank=False, null=False)
    avatar = models.ImageField(upload_to='media/avatars', default='media/default-avatar/avatar1.png')
    bio = models.TextField()


class Room(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=50, blank=False, null=False)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)


class Category(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=255, blank=True, null=False)
    is_payment = models.BooleanField(default=False, blank=False, null=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='category_in_room', blank=False, null=False)


class Task(models.Model):
    id = models.IntegerField().primary_key
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_important = models.BooleanField(default=False, blank=False, null=False)
    is_completed = models.BooleanField(default=False, blank=False, null=False)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_completed_by_user', blank=True, null=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created_by_user', blank=False, null=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=False)
    completion_time = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    completion_comment = models.CharField(blank=True, null=True, max_length=255)


class UserRoom(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    can_create_task = models.BooleanField(default=False, blank=False, null=False)
    can_finish_task = models.BooleanField(default=False, blank=False, null=False)
