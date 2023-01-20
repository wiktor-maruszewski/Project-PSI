import string
from datetime import datetime
from rest_framework import serializers
from ToDoApp.models import Task, Category, Room, UserRoom, Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'avatar', 'bio']

    # def validate_nickname(self, value):
    #     if not value:
    #         raise serializers.ValidationError(
    #             'Your nickname cannot be empty'
    #         )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_payment', 'room_id']

    # def validate_name(self, value):
    #     if not value:
    #         value = 'General'
    #     charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
    #     if any(letter not in charset_list for letter in value):
    #         raise serializers.ValidationError(
    #             "Your category name must not contain invalid characters (only letters, numbers and symbols)!",
    #         )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_date(self):
        if self.get_value('start_time') < datetime.today():
            raise serializers.ValidationError(
                "The task start time cannot be set before the current time.")

        if self.data.get('start_time') < self.data.get('end_time'):
            raise serializers.ValidationError(
                "The task end time cannot be set before the start time.")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'creator_id']
    #
    # def validate_name(self, value):
    #     charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
    #     if any(letter not in charset_list for letter in value):
    #         raise serializers.ValidationError(
    #             "Your room name must not contain invalid characters (only letters, numbers and symbols)!",
    #         )


class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = ['user_id', 'room_id', 'is_admin', 'can_create_task', 'can_finish_task']