from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from users.models import User


class AbstractTask(models.Model):
    """Базовая модель Задачи с требуемыми полями."""
    class TaskStatus(models.TextChoices):
        NEW = 'NEW', _('Новая')
        PLANNED = 'PLANNED', _('Запланированная')
        IN_WORK = 'IN_WORK', _('В работе')
        COMPLETED = 'COMPLETED', _('Завершённая')

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    add_date = models.DateTimeField('Дата создания', auto_now_add=True)

    status = models.CharField(
        max_length=100, choices=TaskStatus.choices, default=TaskStatus.NEW,
        verbose_name='Статус', blank=True)

    completion_date = models.DateTimeField(
        'Планируемая дата завершения', blank=True, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        abstract = True


class Task(AbstractTask):
    """
    Рабочая модель Задачи наследуемая от базовой с
    переопределенным сохранением.
    """
    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        При сохранении задачи создается ее копия в модели TaskHistory
        для хранения истории изменений.
        """
        super(Task, self).save(*args, **kwargs)
        TaskHistory.objects.create(
            title=self.title, description=self.description,
            add_date=self.add_date, status=self.status,
            completion_date=self.completion_date, user=self.user, task=self)

    class Meta:
        ordering = ('-add_date', )


class TaskHistory(AbstractTask):
    """
    Модель для хранения истории изменений задачи, наследуется от базовой.
    Дополнена ссылкой на рабочую задачу и полем с временем изменения.
    """
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='history',
        verbose_name='Задача')

    edit_time = models.DateTimeField('Дата изменения', auto_now_add=True)

    class Meta:
        ordering = ('-edit_time', '-id', )
