from django.contrib import admin
from .models import Message, Client, Mailing

# Register your models here.

admin.site.register(Message)
admin.site.register(Client)
admin.site.register(Mailing)