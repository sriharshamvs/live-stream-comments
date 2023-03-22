"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "live-stream-comments.settings")
django.setup()

from comments.models import ChannelSession
import datetime
from django.core import serializers

sessions = ChannelSession.objects.filter(online=True)
full_time = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
file_name = f"sessions/{full_time}.json"
with open(file_name,'w') as f:
    data = serializers.serialize("json", sessions)
    f.write(data)
session_count = len(sessions)
print(f"Wrote {session_count} previous stale sessions to {file_name}")
sessions.delete()
print(f"Deleted {session_count} Stale Channel Sessions")

application = get_default_application()
