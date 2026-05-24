"""
Добавляет поля аутентификации к модели EventUser:
- password  — хэш пароля (PBKDF2)
- role      — роль пользователя (user / admin)
- created_at — дата регистрации

Для существующих строк: password='', role='user', created_at=now().
"""

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_participant_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventuser',
            name='password',
            field=models.CharField(max_length=128, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventuser',
            name='role',
            field=models.CharField(
                max_length=10,
                choices=[('user', 'Пользователь'), ('admin', 'Администратор')],
                default='user',
            ),
        ),
        migrations.AddField(
            model_name='eventuser',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
    ]
