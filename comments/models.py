from django.db import models

# Create your models here.
class ChannelMessage(models.Model):
    channel_name = models.CharField(max_length=2000)
    user_id = models.CharField(max_length=2000)
    user_name = models.CharField(max_length=2000)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField()
    pinned = models.BooleanField()

