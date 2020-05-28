from django.contrib import admin
from  .models import  ChannelMessage, Channel, IPAddress
from django.utils.html import format_html
# Register your models here.

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'moderate', 'channel_url')
    def channel_url(self, obj):
        return format_html(f"<a href='/{obj.channel_name}/moderate'>/{obj.channel_name}/moderate</a>")
    channel_url.allow_tags = True
    channel_url.short_description = "Moderation URL"

admin.site.register(Channel, ChannelAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked')

admin.site.register(IPAddress, IPAddressAdmin)

class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'message', 'ip_address', 'user_name', 'pinned', 'approved')
    list_filter = ['channel', 'ip_address', 'user_name']

admin.site.register(ChannelMessage, ChannelMessageAdmin)
