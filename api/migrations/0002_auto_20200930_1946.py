# Generated by Django 3.1.1 on 2020-09-30 16:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltask',
            name='completion_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Планируемая дата завершения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='completion_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 30, 16, 46, 0, 37708, tzinfo=utc), verbose_name='Планируемая дата завершения'),
            preserve_default=False,
        ),
    ]
