# Generated by Django 4.2.8 on 2023-12-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='Ник в телеграме'),
        ),
    ]
