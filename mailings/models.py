from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Mailing(models.Model):
    date_time_start_mailing = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    date_time_end_mailing = models.DateTimeField(verbose_name='Дата и время окончания рассылки', blank=True, null = True)
    text_message = models.TextField(verbose_name='Текст сообщения', blank=True, null=True)
    filter = models.CharField(verbose_name='Фильтр по тегу или коду оператора', max_length= 100, blank=True, null=True )


    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        if self.date_time_end_mailing and self.filter:
            return f'Рассылка id => {self.pk} с тегом => {self.filter} начало рассылки => {self.date_time_start_mailing} окончание рассылки => {self.date_time_end_mailing}'
        elif self.filter:
            return f'Рассылка id => {self.pk} с тегом => {self.filter} начало рассылки => {self.date_time_start_mailing}'
        elif self.date_time_end_mailing:
            return f'Рассылка id => {self.pk} начало рассылки => {self.date_time_start_mailing} окончание рассылки => {self.date_time_end_mailing}'
        else:
            return f'Рассылка id => {self.pk} начало рассылки => {self.date_time_start_mailing}'


class Client(models.Model):
    validator_for_phone_number = RegexValidator(regex=r'7\d{10}$', message='Формат номера -> 7(XXX)XXXXXXX, где X это цифра от 0 до 9')
    phone_number = models.CharField(verbose_name='Номер телефона', unique=True, max_length = 11, validators=[validator_for_phone_number,])
    operator_code = models.CharField(verbose_name='Код оператора', max_length=3, blank=True, null=True)
    tag = models.CharField(verbose_name='Тег', max_length= 100, blank=True, null=True )
    timezone = models.IntegerField(verbose_name='Часовой пояс ', validators=[MinValueValidator(0), MaxValueValidator(23)])

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        if self.tag:
            return f'Клиент c id => {self.pk} и тегом => {self.tag}'
        else:
            return f'Клиент c id => {self.pk}'

class Message(models.Model):
    date_time_create = models.DateTimeField(verbose_name='Дата создания сообщения', auto_created=True)
    status = models.JSONField(verbose_name="Статус отправки", blank=True, null=True)
    mailing = models.ForeignKey('Mailing', verbose_name='Рассылка', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey('Client', verbose_name='Клиент', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        if self.status:
            return f'Сообщение id => {self.pk} статус отправки => {self.status}'
        else:
            return f'Сообщение id => {self.pk}'
