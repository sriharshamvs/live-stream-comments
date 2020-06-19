from django.db import models
from django.contrib.auth.models import User # importing default django user models

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
        
        
class ChannelViewer(models.Model):
    name = models.CharField(max_length=2000)
    place = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=2000)
    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class ChannelSession(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=2000)
    user_name = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    online = models.BooleanField()
    
    def __str__(self):
        return f"{self.user_name} - {self.channel} - {self.online}"

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
        return self.channel.channel_name


class ChannelMod(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT) # We will not enable channel deletion from moderation model Why?
    users = models.ManyToManyField(User)

    def __str__(self):
        user_names = ",".join([x.username for x in self.users.all()])
        return f"{self.channel} can be accessed by {user_names}"
    
