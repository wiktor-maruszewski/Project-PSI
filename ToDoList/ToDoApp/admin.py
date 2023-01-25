from django.contrib import admin
from .models import Task, Category, Room, Profile

admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Profile)