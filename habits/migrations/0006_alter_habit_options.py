# Generated by Django 5.0 on 2023-12-19 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_alter_habit_linked_habit_alter_habit_reward'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habit',
            options={'ordering': ('id',), 'verbose_name': 'Привычка', 'verbose_name_plural': 'Привычки'},
        ),
    ]