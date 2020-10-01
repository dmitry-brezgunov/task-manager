from django.utils import timezone
from rest_framework import serializers

from .models import Task, TaskHistory, User


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор модели User для регистрации пользователей'''

    class Meta:
        fields = ('username', 'password', )
        write_only_fields = ('password', )
        model = User

    def create(self, validated_data):
        '''Переопределение метода создания для корректного сохранения пароля'''

        return User.objects.create_user(**validated_data)


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        '''Переопределение представления поля ChoiceField для вывода
        читаемого названия опций в json ответе'''

        return self._choices[obj]


class TaskSerializer(serializers.ModelSerializer):
    '''Сереализатор модели Task c выводом
    читаемого названия опций в json ответе'''

    status = ChoiceField(choices=Task.TaskStatus.choices, required=False)

    def validate(self, data):
        '''Валидация даты выполнения задачи. Она не может быть раньше текущей
        даты при создании новой задачи и раньше даты создания при
        изменении задачи'''

        if self.instance:
            if (data.get('completion_date') and
               data['completion_date'] < self.instance.add_date):

                raise serializers.ValidationError(
                    'Дата завершения не может быть раньше даты создания')
        else:
            if (data.get('completion_date') and
               data['completion_date'] < timezone.now()):

                raise serializers.ValidationError(
                    'Дата завершения не может быть раньше текущей даты')
        return data

    class Meta:
        fields = (
            'id', 'title', 'description', 'add_date', 'status',
            'completion_date', )

        model = Task


class TaskHistorySerializer(serializers.ModelSerializer):
    '''Сериализатор модели TaskHistory для вывода истории изменения задачи'''

    status = ChoiceField(choices=Task.TaskStatus.choices, required=False)

    class Meta:
        fields = (
            'title', 'description', 'add_date', 'status',
            'completion_date', 'edit_time', 'task', )
        model = TaskHistory
