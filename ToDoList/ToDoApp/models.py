from django.db import models
import datetime


class Category(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=255)
    is_payment = models.BooleanField(default=False)


class User(models.Model):
    id = models.IntegerField().primary_key
    login = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=32, blank=False, null=False)
    sign_up_date = models.DateField(default=datetime.date.today, null=False)
    nickname = models.CharField(max_length=30)


class Room(models.Model):
    id = models.IntegerField().primary_key
    name = models.CharField(max_length=50)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    id = models.IntegerField().primary_key
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_important = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_completed_by_user')
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created_by_user')
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    completion_time = models.DateTimeField(default=datetime.date.today)
    completion_comment = models.CharField(max_length=255)


class User_room(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    can_create_task = models.BooleanField(default=False)
    can_finish_task = models.BooleanField(default=False)
