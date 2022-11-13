import string
from datetime import datetime

from rest_framework import serializers
from ToDoApp.models import User, Task
from ToDoApp.models import Category
from ToDoApp.models import Room
from ToDoApp.models import UserRoom


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_login(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Your login must not be less than 5 characters long!",
            )

        charset_list = [*string.ascii_letters, *string.digits]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your login must not contain invalid characters (only letters and numbers)!",
            )

    def validate_nickname(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Your nickname must not be less than 5 characters long!",
            )

        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your nickname must not contain invalid characters (only letters, numbers and symbols)!",
            )

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Your nickname must not be less than 8 characters long!",
            )

        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your password must not contain invalid characters (only letters, numbers and symbols)!",
            )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            value = 'General'
        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your category name must not contain invalid characters (only letters, numbers and symbols)!",
            )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_start_time(self, value):
        if value < datetime.now():
            raise serializers.ValidationError(
                "The task start time cannot be set before the current time.",
            )

    def validate_end_time(self, value):
        if value < self.get_value('start_time'):
            raise serializers.ValidationError(
                "The task end time cannot be set before the start time.",
            )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def validate_name(self, value):
        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your room name must not contain invalid characters (only letters, numbers and symbols)!",
            )


class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoom
        fields = '__all__'
