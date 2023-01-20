from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=False, null=False)
    avatar = models.ImageField(upload_to='../../media/avatars', default='/ToDoList/ToDoApp/static/media/default-avatar/avatar1.png')
    bio = models.TextField()


    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


    def __str__(self):
        return "Profil " + self.user.username + ": " + self.nickname


class Room(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)


    class Meta:
        verbose_name = 'Pokój'
        verbose_name_plural = 'Pokoje'


    def __str__(self):
        return 'Pokoj: ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=False)
    is_payment = models.BooleanField(default=False, blank=False, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='category_in_room', blank=False, null=False)


    class Meta:
            verbose_name = 'Kategoria'
            verbose_name_plural = 'Kategorie'


    def __str__(self):
        return 'Kategoria: ' + self.name + " | pokoj: " + self.room.name


class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_important = models.BooleanField(default=False, blank=False, null=False)
    is_completed = models.BooleanField(default=False, blank=False, null=False)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_tasks', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', blank=True, null=True)
    completion_time = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    completion_comment = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'


    def __str__(self):
        t = Task.objects.get(id=self.id)
        return 'Task: ' + str(t.id) + " | kategoria: " + self.category.name + " | pokoj: " + self.category.room.name


class UserRoom(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    room= models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    can_create_task = models.BooleanField(default=False, blank=False, null=False)
    can_finish_task = models.BooleanField(default=False, blank=False, null=False)
