from django.contrib import admin
from  .models import  ChannelMessage, Channel, IPAddress, ChannelMod, ChannelSession, ChannelViewer
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import naturaltime
# Register your models here.

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'moderate', 'channel_url', 'export_url')
    def channel_url(self, obj):
        return format_html(f"<a href='/{obj.channel_name}/moderate' target='_blank'>/{obj.channel_name}/moderate</a>")
    def export_url(self, obj):
        return format_html(f"<a href='/export/{obj.channel_name}' target='_blank'>/export/{obj.channel_name}</a>")
    channel_url.allow_tags = True
    channel_url.short_description = "Moderation URL"
    export_url.allow_tags = True
    export_url.short_description = "Export URL"

admin.site.register(Channel, ChannelAdmin)

class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked')
    search_fields = ('ip_address',)

admin.site.register(IPAddress, IPAddressAdmin)

class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'message', 'ip_address', 'user_name', 'pinned', 'approved')
    list_filter = ['channel']
    search_fields = ['user_name']


class ChannelModAdmin(admin.ModelAdmin):
    pass
    

def naturalTimeDifference(delta):
        if delta.days >= 1:
            return deta.days + " days"
        elif delta.seconds > 3600:
            return str(round(delta.seconds / 3600,2)) + ' hours'  # 3 hours ago
        elif delta.seconds >  60:
            return str(round(delta.seconds/60,2)) + ' minutes'     # 29 minutes ago
        else:
            return str(delta.seconds) + " seconds"                             # a moment ago
        
   
class ChannelSessionAdmin(admin.ModelAdmin):
    list_display = ('channel', 'user_id', 'user_name', 'online', 'created_at', 'ended_at', 'duration')

    def duration(self, obj):
        if obj.ended_at:
            return naturalTimeDifference(obj.ended_at - obj.created_at)
        else:
            return '-'
    duration.allow_tags = True
    duration.short_description = "Duration"
    
class ChannelViewerAdmin(admin.ModelAdmin):
    pass

admin.site.register(ChannelMod, ChannelModAdmin)
admin.site.register(ChannelMessage, ChannelMessageAdmin)
admin.site.register(ChannelViewer, ChannelViewerAdmin)
admin.site.register(ChannelSession, ChannelSessionAdmin)
