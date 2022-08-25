from django.contrib.postgres.indexes import HashIndex
from django.core import validators
from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
import pytz


class Mailing(models.Model):
    """ Рассылка """
    datetime_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    text = models.TextField(verbose_name='Текст сообщения')
    filter_code = models.CharField(
        verbose_name='Код мобильного оператора для фильтрации',
        max_length=3,
        validators=[validators.RegexValidator(regex=r'\d{3}')]
    )
    filter_tag = models.CharField(
        verbose_name='Тег для фильтрации',
        max_length=255
    )
    datetime_end = models.DateTimeField(verbose_name='Дата и время окончания рассылки')

    class Meta:
        db_table = 'mailings'

class Client(models.Model):
    """ Клиент """
    phone = models.CharField(
        verbose_name='Номер телефона',
        unique=True,
        max_length=11,
        validators=[validators.RegexValidator(regex=r'^7\d{10}$')]
    )
    code = models.CharField(
        verbose_name='Код мобильного оператора',
        max_length=3,
        validators=[validators.RegexValidator(regex=r'\d{3}')]
    )
    tag = models.CharField(
        verbose_name='Тег',
        max_length=255
    )
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(
        verbose_name='Часовой пояс',
        max_length=32,
        choices=TIMEZONES,
        default='UTC'
    )

    class Meta:
        db_table = 'clients'
        indexes = [
            models.Index(fields=('code', 'tag'),
                         name='i_client_code_tag'),
        ]

    def __str__(self):
        return self.phone

class Message(models.Model):
    """ Сообщение """
    created = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )
    is_sent = models.BooleanField(
        verbose_name='Статус отправки',
        default=False
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
        related_name='mailing_messages'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент получатель',
        related_name='client_messages'
    )

    class Meta:
        db_table = 'messages'
        indexes = [
            HashIndex(fields=['is_sent'],
                      name='i_message_is_sent'),
        ]
