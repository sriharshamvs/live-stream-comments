from django.db import models


class Channel(models.Model):
    channel_name = models.CharField(max_length=2000)
    moderate = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.channel_name
    
class IPAddress(models.Model):
    ip_address = models.CharField(max_length=200)
    blocked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ip_address

# Create your models here.
class ChannelMessage(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=2000)
    user_name = models.CharField(max_length=2000)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField()
    pinned = models.BooleanField()
    approved = models.BooleanField()
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    def __str__(self):
        return self.channel
