import datetime
import string
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Task, Category, Room, Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='profile-detail', read_only=True)
    username = serializers.StringRelatedField(source='user.username')
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = Profile
        fields = ('url', 'nickname', 'avatar', 'bio', 'username', 'user')

    def validate_nickname(self, value):
        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your nickname must not contain invalid characters (only letters, numbers and symbols)!",
            )
        return value


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    room = serializers.HyperlinkedRelatedField(queryset=Room.objects.all(), view_name='room-detail')

    class Meta:
        model = Category
        fields = ('url', 'name', 'room_name', 'room', 'is_payment')


class TaskListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='task-detail', read_only=True)
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    end_time = serializers.DateTimeField()
    start_time = serializers.DateTimeField()

    category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')

    def validate(self, data):
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)

        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time.")

        if start_time and start_time < datetime.datetime.now():
            raise serializers.ValidationError("Start time must be in the future.")

        return data

    class Meta:
        model = Task
        fields = ('url', 'category', 'created_by', 'description', 'start_time', 'end_time', 'is_important')


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='task-detail', read_only=True)

    category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    end_time = serializers.DateTimeField(required=False)
    start_time = serializers.DateTimeField(required=False)

    completion_time = serializers.DateTimeField(read_only=True)
    completed_by = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    def validate(self, data):
        start_time = data.get('start_time', None)
        end_time = data.get('end_time', None)
        is_completed = data.get('is_completed', None)
        completion_comment = data.get('completion_comment', None)

        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError("End time must be after start time.")

        if start_time and start_time < datetime.datetime.now():
            raise serializers.ValidationError("Start time must be in the future.")

        if not is_completed and completion_comment:
            raise serializers.ValidationError(
                "Can't add completion comment if task is not completed.")

        return data

    def update(self, instance, validated_data):
        request = self.context.get("request").user

        if validated_data.get('is_completed', None):
            validated_data["completed_by"] = request
            validated_data['completion_time'] = timezone.now()
        else:
            validated_data['completed_by'] = None
            validated_data['completion_time'] = None

        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = (
            'url', 'category', 'created_by', 'description', 'start_time', 'end_time', 'is_important', 'is_completed',
            'completed_by', 'completion_time', 'completion_comment')


class RoomListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='room-detail', read_only=True)

    categories = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='category-detail',
        read_only=True,
        source='category_set'
    )

    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )

    can_create_task = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        read_only=True
    )

    can_finish_task = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name='user-detail',
    )

    is_moderator = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        read_only=True
    )

    user_room = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        queryset=User.objects.all(),
    )

    creator_username = serializers.CharField(source='creator.username', read_only=True)

    def validate_name(self, value):
        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your room name must not contain invalid characters (only letters, numbers and symbols)!",
            )
        return value

    class Meta:
        model = Room
        fields = (
            'url', 'name', 'creator_username', 'creator', 'can_create_task', 'can_finish_task', 'is_moderator',
            'user_room',
            'categories')


class RoomDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='room-detail', read_only=True)

    categories = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='category-detail',
        read_only=True,
        source='category_set'
    )

    creator = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )

    can_create_task = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        queryset=User.objects.all(),
    )

    can_finish_task = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        many=True,
        view_name='user-detail',
    )

    is_moderator = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        queryset=User.objects.all(),
    )

    user_room = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='user-detail',
        queryset=User.objects.all(),
    )

    creator_username = serializers.CharField(source='creator.username', read_only=True)

    def update(self, instance, validated_data):
        for user in validated_data['can_create_task']:
            if not (user in validated_data['user_room']):
                raise serializers.ValidationError(
                    "Those users cannot create a task because they are not in this room!",
                )

        for user in validated_data['can_finish_task']:
            if not (user in validated_data['user_room']):
                raise serializers.ValidationError(
                    "Those users cannot finish a task because they are not in this room!",
                )

        for user in validated_data['is_moderator']:
            if not (user in validated_data['user_room']):
                raise serializers.ValidationError(
                    "Those users cannot be a moderator because they are not in this room!",
                )

        return super().update(instance, validated_data)

    def validate_name(self, value):
        charset_list = [*string.ascii_letters, *string.digits, *string.printable[62:-6]]
        if any(letter not in charset_list for letter in value):
            raise serializers.ValidationError(
                "Your room name must not contain invalid characters (only letters, numbers and symbols)!",
            )
        return value

    class Meta:
        model = Room
        fields = (
            'url', 'name', 'creator_username', 'creator', 'can_create_task', 'can_finish_task', 'is_moderator',
            'user_room',
            'categories')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    rooms = RoomListSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)
    profile_url = serializers.HyperlinkedRelatedField(source='profile', read_only=True, view_name='profile-detail')

    def create(self, validated_data):
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = make_password(validated_data['password'])
        validated_data['password'] = password
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'email', 'password', 'profile', 'profile_url', 'tasks', 'categories',
                  'rooms']
