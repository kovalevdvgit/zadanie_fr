from rest_framework import serializers
from .models import Client, Mailing, Message

class Serializator_for_Client(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone_number', 'operator_code', 'tag', 'timezone', 'message_set')



class Serializator_for_Mailing(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

class Serializator_for_Message(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'