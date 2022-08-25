from rest_framework import serializers

from .models import (
    Client,
    Mailing,
    Message,
)


class ClientSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления нового клиента """

    class Meta:
        model = Client
        fields = '__all__'

class MailingSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления новой рассылки """

    class Meta:
        model = Mailing
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    """ Сериализатор сообщения """
    client = serializers.SlugRelatedField(read_only=True, slug_field='phone')

    class Meta:
        model = Message
        fields = '__all__'

class TotalStatisticMailingSerializer(serializers.Serializer):
    """ Сериализатор общей статистики по рассылкам """
    mailing = MailingSerializer()
    amount_sent_messages = serializers.IntegerField()
    amount_not_sent_messages = serializers.IntegerField()

class DetailStatisticMailingSerializer(serializers.Serializer):
    """ Сериализатор детальной статистики по конкретной рассылке """
    mailing = MailingSerializer()
    messages = MessageSerializer(many=True)