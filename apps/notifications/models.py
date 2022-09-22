from django.contrib.postgres.indexes import HashIndex
from django.core import validators
from django.db import models
import pytz


class Mailing(models.Model):
    """ Рассылка """
    datetime_start = models.DateTimeField(
        verbose_name='Дата и время запуска рассылки'
    )
    text = models.TextField(
        verbose_name='Текст сообщения'
    )
    filter_code = models.CharField(
        max_length=3,
        validators=[validators.RegexValidator(regex=r'\d{3}')],
        verbose_name='Код мобильного оператора для фильтрации',
    )
    filter_tag = models.CharField(
        max_length=255,
        verbose_name='Тег для фильтрации',
    )
    datetime_end = models.DateTimeField(
        verbose_name='Дата и время окончания рассылки'
    )

    class Meta:
        db_table = 'mailings'

class Client(models.Model):
    """ Клиент """
    phone = models.CharField(
        unique=True,
        max_length=11,
        validators=[validators.RegexValidator(regex=r'^7\d{10}$')],
        verbose_name='Номер телефона',
    )
    code = models.CharField(
        max_length=3,
        validators=[validators.RegexValidator(regex=r'\d{3}')],
        verbose_name='Код мобильного оператора',
    )
    tag = models.CharField(
        max_length=255,
        verbose_name='Тег',
    )
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONES,
        default='UTC',
        verbose_name='Часовой пояс',
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
        auto_now_add=True,
        verbose_name='Дата и время создания',
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name='Статус отправки',
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='mailing_messages',
        verbose_name='Рассылка',
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='client_messages',
        verbose_name='Клиент получатель',
    )

    class Meta:
        db_table = 'messages'
        indexes = [
            HashIndex(fields=['is_sent'],
                      name='i_message_is_sent'),
        ]
