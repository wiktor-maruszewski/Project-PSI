# Generated by Django 4.1.5 on 2023-01-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoApp', '0003_room_user_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
