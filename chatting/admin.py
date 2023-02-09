from django.contrib import admin
from chatting.models import *

# Register your models here.

class CustomRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user_created", )
    ordering = ('name',)

    def user_created(self, obj):
        return obj.username

admin.site.register(RoomUsers)
admin.site.register(Message)
admin.site.register(Room, CustomRoomAdmin)
