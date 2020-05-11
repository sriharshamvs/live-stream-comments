from django.contrib import admin
from  .models import  ChannelMessage, Channel, IPAddress
# Register your models here.

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'moderate')

admin.site.register(Channel, ChannelAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked')

admin.site.register(IPAddress, IPAddressAdmin)

class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'message', 'ip_address', 'user_name', 'pinned', 'approved')
    list_filter = ['channel', 'ip_address', 'user_name']

admin.site.register(ChannelMessage, ChannelMessageAdmin)
