# Generated by Django 3.1.1 on 2020-10-02 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskhistory',
            options={'ordering': ('-edit_time', '-id')},
        ),
    ]