from django.contrib import admin

from .models import Chat, Participant, Message

admin.site.register(Chat)
admin.site.register(Participant)
admin.site.register(Message)
