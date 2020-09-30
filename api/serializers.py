from django.utils import timezone
from rest_framework import serializers

from .models import Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'password', )
        write_only_fields = ('password', )
        model = User

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class TaskSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=Task.TaskStatus.choices)

    class Meta:
        fields = (
            'id', 'title', 'description', 'add_time', 'status',
            'completion_date', )
        model = Task

    def validate(self, data):
        if not data.get('completion_date'):
            return data

        elif data.get('completion_date') < timezone.now():
            raise serializers.ValidationError(
                'Дата выполнения не может быть меньше текущей')

        return data
