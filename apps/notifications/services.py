from collections import namedtuple
from django.db.models import Count, IntegerField, Q
from django.utils import timezone

from .tasks import create_and_send_messages_for_mailing


def _time_check_and_task_creation(mailing):
    """  """
    date_time = timezone.localtime(timezone.now())
    if (mailing.datetime_start <= date_time) and (mailing.datetime_end >= date_time):
        create_and_send_messages_for_mailing.delay(mailing.pk, mailing.filter_code, mailing.filter_tag, mailing.datetime_end)
    else:
        create_and_send_messages_for_mailing.apply_async(
            (mailing.pk, mailing.filter_code, mailing.filter_tag, mailing.datetime_end),
            eta=mailing.datetime_start,
            task_id=str(mailing.pk)
        )

def _get_mailings_list_with_statistic_sent_messages(mailings):
    """ Получение списка рассылок со статистикой
    отправленных сообщений по каждой из рассылки """
    total_list = []
    for mailing in mailings:
        statistic = namedtuple('statistic', ('mailing', 'amount_sent_messages', 'amount_not_sent_messages'))
        sent_messages = mailing.mailing_messages.aggregate(amount=Count('pk',
                                                                        output_field=IntegerField(),
                                                                        filter=Q(is_sent=True)))
        not_sent_messages = mailing.mailing_messages.aggregate(amount=Count('pk',
                                                                            output_field=IntegerField(),
                                                                            filter=Q(is_sent=False)))
        stat = statistic(
            mailing=mailing,
            amount_sent_messages=sent_messages['amount'],
            amount_not_sent_messages=not_sent_messages['amount']
        )
        total_list.append(stat)

    return total_list

