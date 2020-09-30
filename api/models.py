from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

User = get_user_model()


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        NEW = 'NEW', _('Новая')
        PLANNED = 'PLANNED', _('Запланированная')
        IN_WORK = 'IN_WORK', _('В работе')
        COMPLETED = 'COMPLETED', _('Завершённая')

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    add_time = models.DateTimeField('Время создания', auto_now_add=True)

    status = models.CharField(
        max_length=100, choices=TaskStatus.choices, default=TaskStatus.NEW,
        verbose_name='Статус')

    completion_date = models.DateTimeField(
        'Планируемая дата завершения', blank=True, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='task',
        verbose_name='Пользователь')

    history = HistoricalRecords()

    class Meta:
        ordering = ('-add_time', )
