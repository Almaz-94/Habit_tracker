# Generated by Django 5.0 on 2023-12-13 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, max_length=150, null=True, verbose_name='место')),
                ('time', models.TimeField(verbose_name='во сколько выполнять привычку')),
                ('action', models.CharField(max_length=200, verbose_name='действие')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='приятная')),
                ('period', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='периодичность в днях')),
                ('reward', models.CharField(blank=True, max_length=200, null=True, verbose_name='награда')),
                ('duration_time', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='время на выполнение')),
                ('is_public', models.BooleanField(default=False, verbose_name='публичная')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='создатель')),
                ('linked_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habit', verbose_name='связанная привычка')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]