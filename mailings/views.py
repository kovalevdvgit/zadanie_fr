import logging
from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import Serializator_for_Client, Serializator_for_Mailing, Serializator_for_Message
from .models import Client, Message, Mailing

logger = logging.getLogger('log')
handler = logging.FileHandler(filename='log_2.txt')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

#=======================================================================================================================Контроллеры для Клиентов
class client_setting(generics.RetrieveUpdateDestroyAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = Serializator_for_Client

    def perform_update(self, serializer):
        client = serializer.save()
        logger.info(f'obj => client, id => {client.pk}, metod => put, time  => {timezone.now()}, info => updated')


    def perform_destroy(self, serializer):
        logger.info(f'obj => client, id => {serializer.pk}, metod => delete, time  => {timezone.now()}, info => deleted')
        serializer.delete()

class client_create(generics.CreateAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = Serializator_for_Client


    def perform_create(self, serializer):
        client = serializer.save()
        logger.info(f'obj => client, id => {client.pk} , metod => post, time  => {timezone.now()}, info => created')

class client_view(generics.ListAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = Serializator_for_Client

#=======================================================================================================================Контроллеры для Рассылок
class mailing_setting(generics.RetrieveUpdateDestroyAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = Serializator_for_Mailing


    def perform_update(self, serializer):
        mailing = serializer.save()
        logger.info(f'obj => mailing, id => {mailing.pk}, metod => put, time  => {timezone.now()}, info => updated')


    def perform_destroy(self, serializer):
        logger.info(f'obj => mailing, id => {serializer.pk}, metod => delete, time  => {timezone.now()}, info => deleted')
        serializer.delete()

class mailing_create(generics.CreateAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = Serializator_for_Mailing

class mailing_view(generics.ListAPIView):
#class Crud_for_client(generics.ListCreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = Serializator_for_Mailing

#=======================================================================================================================Статистика

class statistic_all(APIView):
    def get(self, request):
        mailings = Mailing.objects.all().count()
        messages = Message.objects.all().count()
        clients = Client.objects.all().count()

        st0 = Message.objects.filter(status__code = 0).count()
        st1 = Message.objects.filter(status__code = 1).count()
        st2 = Message.objects.filter(status__code = 2).count()
        st3 = Message.objects.filter(status__code = 3).count()


        info = {
                "created_mailings":mailings,
                'all_clients':clients,
                'created_all_message':messages,
                'good mailing, delivered messages':st0,
                'late mailing, delivered messages':st1,
                'good mailing, not delivered messages':st2,
                'late mailing, not delivered messages':st3,}
        return Response(info)

class statistic(APIView):
    def get(self, request, pk):
        try:
            obj_mailing = Mailing.objects.get(pk = pk)
            obj_messages = obj_mailing.message_set

            messages = obj_messages.count()
            clients = (Client.objects.filter(tag = obj_mailing.filter) or Client.objects.filter(operator_code  = obj_mailing.filter)).count()

            st0 = obj_messages.filter(status__code=0).count()
            st1 = obj_messages.filter(status__code=1).count()
            st2 = obj_messages.filter(status__code=2).count()
            st3 = obj_messages.filter(status__code=3).count()

            info = {
                'current mailing': str(obj_mailing),
                'clients': clients,
                'created_all_message': messages,
                'good mailing, delivered messages': st0,
                'late mailing, delivered messages': st1,
                'good mailing, not delivered messages': st2,
                'late mailing, not delivered messages': st3,
            }
        except:
            info = {'code':4,
                    'information': 'The porblem with extracting the mailing or mailing with numbers does not exist'}
        return Response(info)









