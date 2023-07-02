import datetime

from django.test import TestCase
from .models import Mailing, Client, Message

from http import HTTPStatus
import json

# Create your tests here.
class Test(TestCase):

    def test_client(self):
        #===============================================================================================================Добавить данные в БД
        phone_number = '79009009090'
        operator_code = '900'
        tag = 'tag'
        timezone = 5
        test_client = Client( phone_number = phone_number, operator_code=operator_code, tag=tag, timezone=timezone)
        self.assertEquals(test_client.phone_number, phone_number)
        self.assertEquals(test_client.operator_code, operator_code)
        self.assertEquals(test_client.tag, tag)
        self.assertEquals(test_client.timezone, timezone)

        date_time_start_mailing = datetime.datetime.now()
        date_time_end_mailing = datetime.datetime.now()
        text_message = 'For test'
        filter = 'tag'
        test_mailing = Mailing(date_time_start_mailing = date_time_start_mailing, date_time_end_mailing = date_time_end_mailing , text_message = text_message, filter = filter )
        self.assertEquals(test_mailing.date_time_start_mailing, date_time_start_mailing)
        self.assertEquals(test_mailing.date_time_end_mailing, date_time_end_mailing)
        self.assertEquals(test_mailing.text_message, text_message)
        self.assertEquals(test_mailing.filter, filter)




        #===============================================================================================================Тест Клиента
        response = self.client.post('/api/client_create/', { 'phone_number ':phone_number,
                                                             'operator_code':operator_code,
                                                             'tag':tag,
                                                             'timezone':timezone},)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(response.json()['tag'], tag)

        response = self.client.get("/api/client_view/")
        self.assertEquals(response.status_code, HTTPStatus.OK)

        response= self.client.patch("/api/client/1/", json = {'timezone':1,})
        self.assertEquals(response.status_code, HTTPStatus.OK)

        response = self.client.get("/api/client/1/")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.json()['tag'], tag)

        response = self.client.delete("/api/client/1/")
        self.assertEquals(response.status_code, HTTPStatus.NO_CONTENT)
        # ===============================================================================================================Тест Рассылки

        response = self.client.post('/api/mailing_create/', {'date_time_start_mailing ': date_time_start_mailing,
                                                            'date_time_end_mailing': date_time_end_mailing,
                                                            'text_message': text_message,
                                                            'filter': filter}, )
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(response.json()['filter'], filter)


        response = self.client.get("/api/mailing_view/")
        self.assertEquals(response.status_code, HTTPStatus.OK)

        response= self.client.patch("/api/mailing/1/", json = {'filter':'ggg',})
        self.assertEquals(response.status_code, HTTPStatus.OK)

        response = self.client.get("/api/mailing/1/")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.json()['filter'], filter)

        response = self.client.delete("/api/mailing/1/")
        self.assertEquals(response.status_code, HTTPStatus.NO_CONTENT)
        # ===============================================================================================================Тест Рассылки
        response = self.client.get("/api/statistic_all/")
        self.assertEquals(response.status_code, HTTPStatus.OK)

        response = self.client.get("/api/statistic/1/")
        self.assertEquals(response.status_code, HTTPStatus.OK)




