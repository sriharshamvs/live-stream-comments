from django.shortcuts import render, redirect
from .models import ChannelMod, ChannelMessage, ChannelSession
import csv
from django.http import HttpResponse
import json

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    return render(request, 'comments/home.html', {})

def go(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if not request.method == 'POST':
        return redirect('/accounts/login')

    return  redirect(f"/{request.POST['room']}/moderate")
#    return render(request, 'comments/home.html', {})


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    return redirect('/accounts/login')


def naturalTimeDifference(delta):
        if delta.days >= 1:
            return deta.days + " days"
        elif delta.seconds > 3600:
            return str(round(delta.seconds / 3600,2)) + ' hours'  # 3 hours ago
        elif delta.seconds >  60:
            return str(round(delta.seconds/60,2)) + ' minutes'     # 29 minutes ago
        else:
            return str(delta.seconds) + " seconds"            

def exportcsv(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    comments = ChannelMessage.objects.filter(channel__channel_name=room_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{room_name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['User Name', 'Message', 'Created At', 'IP Address', 'Duration'])
    for cm in comments:
        cs = ChannelSession.objects.filter(channel = cm.channel, user_id=cm.user_id, online=False)
        duration = None
        if cs:            
            for cso in cs:
                if not duration:
                    duration = cso.ended_at - cso.created_at
                else:
                    duration += cso.ended_at - cso.created_at
            duration = naturalTimeDifference(duration)
        if not duration:
            duration = 'Not Available'
        writer.writerow([cm.user_name,cm.message,cm.created_at,cm.ip_address.ip_address,duration])

    return response

def moderate(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    cmod = ChannelMod.objects.filter(channel__channel_name = room_name)

    print(request.user)
    
    if cmod:
        cmod = cmod[0]
    if cmod and (request.user not in cmod.users.all()):
        print("Mismatched Permission Matrix")
        return render(request, 'comments/nopermission.html')
    return render(request, 'comments/room_mod.html', {
        'room_name': room_name
    })
