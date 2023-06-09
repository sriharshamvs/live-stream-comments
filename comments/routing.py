from django.urls import re_path

from . import consumers
from . import admin_consumers
from . import count_consumers 

websocket_urlpatterns = [
    re_path(r'ws/comments/(?P<room_name>\w+)/$', consumers.CommentsConsumer),
    re_path(r'ws/count/(?P<room_name>\w+)/$', count_consumers.CountConsumer),
    re_path(r'ws/comments_mod/(?P<room_name>\w+)/$', admin_consumers.CommentsConsumerAdmin),
]
