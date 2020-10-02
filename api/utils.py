from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        """
        Переопределение представления поля ChoiceField для вывода
        читаемого названия опций в json ответе.
        """
        return self._choices[obj]
