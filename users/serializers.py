from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для регистрации пользователей."""
    class Meta:
        fields = ('username', 'password', )
        write_only_fields = ('password', )
        model = User

    def create(self, validated_data):
        """
        Переопределение метода создания для
        корректного сохранения пароля.
        """
        return User.objects.create_user(**validated_data)
