# Generated by Django 3.1.1 on 2020-10-02 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201002_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='api.task', verbose_name='Задача'),
        ),
    ]
