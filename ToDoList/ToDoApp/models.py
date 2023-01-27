from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='media/avatars',
                               default='/media/default-avatar/avatar1.png')
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, unique=True)
    bio = models.TextField()

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return f'Username: {self.user.username} | Nickname: {self.nickname}'


class Room(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    can_create_task = models.ManyToManyField(User, default=False, related_name='can_create_task')
    can_finish_task = models.ManyToManyField(User, default=False, related_name='can_finish_task')
    is_moderator = models.ManyToManyField(User, default=False, related_name='is_moderator')
    user_room = models.ManyToManyField(User, default=False, related_name='user_room')

    class Meta:
        verbose_name = 'Pokój'
        verbose_name_plural = 'Pokoje'

    def __str__(self):
        return 'Pokoj: ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_payment = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return 'Kategoria: ' + self.name + " | pokoj: " + self.room.name


class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=datetime.now, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_important = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False, blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='completed_by')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    completion_time = models.DateTimeField(blank=True, null=True)
    completion_comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'

    def __str__(self):
        t = self.objects.get(id=self.id)
        return 'Task: ' + str(t.id) + " | kategoria: " + self.category.name + " | pokój: " + self.category.room.name
