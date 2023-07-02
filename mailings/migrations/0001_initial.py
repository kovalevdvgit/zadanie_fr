# Generated by Django 4.2.2 on 2023-07-02 15:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Формат номера -> 7(XXX)XXXXXXX, где X это цифра от 0 до 9', regex='7\\d{10}$')], verbose_name='Номер телефона')),
                ('operator_code', models.CharField(blank=True, max_length=3, null=True, verbose_name='Код оператора')),
                ('tag', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тег')),
                ('timezone', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(23)], verbose_name='Часовой пояс ')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_start_mailing', models.DateTimeField(verbose_name='Дата и время начала рассылки')),
                ('date_time_end_mailing', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время окончания рассылки')),
                ('text_message', models.TextField(blank=True, null=True, verbose_name='Текст сообщения')),
                ('filter', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фильтр по тегу или коду оператора')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_create', models.DateTimeField(auto_created=True, verbose_name='Дата создания сообщения')),
                ('status', models.JSONField(blank=True, null=True, verbose_name='Статус отправки')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailings.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailings.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]
