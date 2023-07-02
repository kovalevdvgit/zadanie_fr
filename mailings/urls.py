from django.urls import path

from .views import client_setting, client_create, client_view
from .views import mailing_setting, mailing_create, mailing_view
from .views import statistic_all, statistic
from rest_framework import permissions
from rest_framework.schemas import get_schema_view as schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

yasg_schema_view = get_schema_view(openapi.Info(title="Notification_service",default_version="v1",), public=True,)


urlpatterns = [
    #==========================================================================Маршруты клинтов
    path('client_create/', client_create.as_view(), name='client_create'),
    path('client_view/', client_view.as_view(), name='client_view'),
    path('client/<int:pk>/', client_setting.as_view(), name='client_setting'),
    #==========================================================================Маршруты рассылок
    path('mailing_create/', mailing_create.as_view(), name='mailing_create'),
    path('mailing_view/', mailing_view.as_view(), name='mailing_view'),
    path('mailing/<int:pk>/', mailing_setting.as_view(), name='mailing_setting'),
    #==========================================================================Статистика
    path('statistic_all/', statistic_all.as_view(), name='statistic_all' ),
    path('statistic/<int:pk>/', statistic.as_view(), name='statistic'),
    #==========================================================================Схема API
    path('schema/', schema_view(title='lol')),

]