from datetime import datetime
from django.conf import settings
import requests
from django.core.mail import send_mail
from django.db.models import Count, IntegerField, Q
from django.utils import timezone

from notification_service_backend.celery import app
from .models import (
    Client,
    Mailing,
    Message,
)


@app.task(bind=True)
def create_request(self, message_id, phone, text, datetime_end):
    """ Отправка сообщения на внешний API сервис """
    try:
        is_sent = False
        while not is_sent and datetime.strptime(datetime_end, "%Y-%m-%dT%H:%M:%S%z") >= timezone.localtime(timezone.now()):
            response = requests.post("https://probe.fbrq.cloud/v1/send/{}".format(str(message_id)), json={
                "id": message_id,
                "phone": phone,
                "text": text
            }, headers={'Authorization': 'Bearer {}'.format(settings.JWT_TOKEN)})
            if response.status_code == 200:
                message = Message.objects.get(pk=message_id)
                message.is_sent = True
                message.save()
                is_sent = True
            else:
                raise Exception(str(response.status_code))
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@app.task
def create_and_send_messages_for_mailing(mailing_id, filter_code, filter_tag, mailing_datetime_end):
    """ Создание и отправка сообщений на внешний API сервис """
    clients = Client.objects.filter(code=filter_code, tag=filter_tag)
    mailing = Mailing.objects.get(pk=mailing_id)
    mailing_datetime_end = datetime.strptime(mailing_datetime_end, "%Y-%m-%dT%H:%M:%S%z")
    for client in clients:
        date_time_now = timezone.localtime(timezone.now())
        if date_time_now > mailing_datetime_end:
            break
        message = Message.objects.create(mailing=mailing,
                                         client=client)
        create_request.delay(message.pk, int(client.phone), mailing.text, mailing_datetime_end)

@app.task
def send_message_with_statistic():
    """ Рассылка общей статистики
    на почту раз в сутки """
    mailings = Mailing.objects.filter(datetime_end__lt=timezone.localtime(timezone.now()))
    if not mailings:
        return
    text = ""
    for mailing in mailings:
        sent_messages = mailing.mailing_messages.aggregate(amount=Count('pk',
                                                                        output_field=IntegerField(),
                                                                        filter=Q(is_sent=True)))
        not_sent_messages = mailing.mailing_messages.aggregate(amount=Count('pk',
                                                                            output_field=IntegerField(),
                                                                            filter=Q(is_sent=False)))
        text = text + "Рассылка №{}\n" \
                      "   Дата и время запуска: {}\n" \
                      "   Дата и время окончания: {}\n" \
                      "   Код фильтрации: {}\n" \
                      "   Тег фильтрации: {}\n" \
                      "   \n" \
                      "   Количество отправленных сообщений: {}\n" \
                      "   Количество не отправленных сообщений: {}\n" \
                      "   \n"
        text = text.format(
            str(mailing.id),
            mailing.datetime_start.strftime("%B %d, %Y %H:%M:%S"),
            mailing.datetime_end.strftime("%B %d, %Y %H:%M:%S"),
            mailing.filter_code,
            mailing.filter_tag,
            str(sent_messages['amount']),
            str(not_sent_messages['amount'])
        )
    send_mail(
        'Статистика',
        text,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_RECIPIENT],
        fail_silently=False,
    )