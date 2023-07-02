import time

from django.db.models.signals import post_save
from django.utils import  timezone
from django.core.mail import  settings, EmailMessage

from .models import Mailing, Client, Message
from .views import logger

import threading as th
import logging
import datetime
import time
import requests



logger = logger
lock = th.Lock()
#=======================================================================================================Настройки
#=======================================================================================================Настройки для внешнего API сервера
TOKEN = settings.TOKEN
URL_API = settings.URL_API
first_start = True
resanding = settings.RESANDING
letter = settings.SEND_LETTER
#=======================================================================================================/Настройки для внешнего API сервера
#Формат кода для статистики -> X, где X это чило от 0 до 9
# 0 -> Сообщение успешно отправленно на внешний API сервер, Рассылка действующая
# 1 -> Сообщение успешно отправленно на внешний API сервер, Рассылка просрочена
# 2 -> Нет доступа к внешнему API серверу, Рассылка действующая
# 3 -> Нет доступа к внешнему API серверу, Рассылка просрочена
#... -> Если понадобятся
#=======================================================================================================/Настройки




def send_letter(interrup = 1):
    while letter:
        try:
            sender = EmailMessage(subject='info_about_mailing', body='ALL_INFO_FORM_SERVER', to = [settings.SERVER_EMAIL])
            text = open(str(settings.BASE_DIR)+'/log_2.txt','r')
            file_to_send = open(str(settings.BASE_DIR)+'/file_to_send.txt', 'w')
            for i in text.readlines():
                if 'obj => mailing' in i:
                    file_to_send.write(i)
            file_to_send.close()
            sender.attach_file(settings.BASE_DIR+'file_to_send.txt')
            sender.send()
        except Exception as e:
            pass
        time.sleep(3600*24 * interrup)


def prepare_mailing(sender, **kwargs):
    mailing = kwargs['instance']
    clients = Client.objects.filter(tag = mailing.filter) or Client.objects.filter(operator_code  = mailing.filter)
    auto_mailing(mailing, clients, True)



#-----------------------------------Запуск обработчиков-----------------------------------------------------------------

post_save.connect(receiver=prepare_mailing, sender= Mailing)

if first_start:
    first_start != first_start
    potok_for_send_letter = th.Thread(target=send_letter, args=(0.005,))
    potok_for_send_letter.daemon = True
    potok_for_send_letter.start()


class auto_mailing:

    def __init__(self, mailing, clients, resanding = False):

        self.mailing = mailing
        self.clients =  clients
        self.resanding = resanding
        logger.info(f'obj => mailing, id => {mailing.pk}, metod => post, time  => {timezone.now()}, info => created')
        self.now = timezone.now()
        self.work = True

        potok = th.Thread(target= self.send_mailing)
        potok.daemon = True
        potok.start()
    #===================================================================================================================
    def send_mailing(self, interrup = 10):
        if self.resanding:
            try:
                response = self.to_server(URL_API + '1',
                                     head={'Authorization': f'Bearer {TOKEN}'},
                                     body={
                                         'id': 1,
                                         'phone': 79009009090,
                                         'text': 'message',})
                if response.json()['code'] == 0:
                    pass
                else:
                    raise Exception()
            except Exception as e:
                print(f'metka 3 exception => {e}')
                time.sleep(interrup)
                potok = th.Thread(target=self.send_mailing)
                potok.daemon = True
                potok.start()
                exit(0)

        start = self.mailing.date_time_start_mailing
        end = self.mailing.date_time_end_mailing
        late = False
        print(f'start => {start}\n end=> {end}\n now=>{self.now}')

        if self.mailing.date_time_start_mailing <= self.now and self.now <= self.mailing.date_time_end_mailing:
            pass
        elif self.now < self.mailing.date_time_start_mailing:
            while datetime.datetime.now() <= start:
                time.sleep(interrup)
                print(f'mayak ========={interrup}')
        else:
            logger.warn(f'Созданная рассылка не актуальна по времени!')
            late = True
        # ==============================================================
        try:
            for client in self.clients:
                self.send_message(client, late=late)
        except:
            print('Рассылка была удалена')
    #===================================================================================================================
    def send_message(self, client, late, povtor=3):
        # message = Message(mailing = mailing, client = client, date_time_create=datetime.datetime.now())
        message = Message(mailing=self.mailing, client=client, date_time_create=timezone.now())
        message.save()

        head = {
            'Authorization': f'Bearer {TOKEN}',
        }
        body = {
            'id': client.pk,
            'phone': client.phone_number,
            'text': self.mailing.text_message,
        }

        try:
            request_to_foreign_API = self.to_server(URL_API + f'{client.pk}', head=head, body=body, povtor=3)
            for_message_status = request_to_foreign_API.json()
            if late:
                for_message_status['code'] = 1
        except:

            if self.resanding:
                message.delete()
                potok = th.Thread(target=self.send_mailing)
                potok.daemon = True
                potok.start()
                exit(0)

            if late:
                for_message_status = {'code': 3, 'message': 'Connect failed'}

        message.status = for_message_status
        message.save()
        lock.acquire()
        logger.info(f'obj => message, id => {message.pk} , metod => ---, time  => {timezone.now()}, info => created')
        lock.release()
    def to_server(self, url, head, body, povtor=3):
        povtor = povtor
        while povtor > 0:
            try:
                return requests.post(url, headers=head, json=body)
            except:
                pass
            povtor -= 1
        raise requests.exceptions.ConnectTimeout





