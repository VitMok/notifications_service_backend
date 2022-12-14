from collections import namedtuple
from celery.result import AsyncResult
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .models import (
    Client,
    Mailing,
)
from .serializers import (
    ClientSerializer,
    MailingSerializer,
    TotalStatisticMailingSerializer,
    DetailStatisticMailingSerializer,
)
from .services import (
    _time_check_and_task_creation,
    _get_mailings_list_with_statistic_sent_messages,
)


class ClientCreateView(generics.CreateAPIView):
    """ Добавление нового клиента """
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Просмотр, обновление данных
    клиента, а также его удаление """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class MailingCreateView(generics.CreateAPIView):
    """ Добавление новой рассылки """
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        mailing = serializer.save()
        _time_check_and_task_creation(mailing)

class MailingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Просмотр, обновление данных
    рассылки, а также её удаление """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_update(self, serializer):
        mailing = serializer.save()
        _time_check_and_task_creation(mailing)

    def perform_destroy(self, instance):
        AsyncResult(str(instance.pk)).revoke(terminate=True)
        instance.delete()

class TotalStatisticMailingListView(viewsets.ViewSet):
    """ Получение общей статистики
    по созданным рассылкам """

    def list(self, request):
        mailings = Mailing.objects.all()
        serializer = TotalStatisticMailingSerializer(
            _get_mailings_list_with_statistic_sent_messages(mailings),
            many=True
        )
        return Response(serializer.data)

class DetailStatisticMailingView(generics.ListAPIView):
    """ Получение детальной статистики отправленных
    сообщений по конкретной рассылке """

    def list(self, request, *args, **kwargs):
        mailing = Mailing.objects.prefetch_related('mailing_messages').get(pk=self.kwargs['pk'])
        statistic = namedtuple('statistic', ('mailing', 'messages'))
        stat = statistic(
            mailing=mailing,
            messages=mailing.mailing_messages,
        )
        serializer = DetailStatisticMailingSerializer(stat)
        return Response(serializer.data)

