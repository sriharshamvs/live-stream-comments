from django.shortcuts import render, redirect
from .models import ChannelMod, ChannelMessage
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

def exportcsv(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    comments = ChannelMessage.objects.filter(channel__channel_name=room_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{room_name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['User Name', 'Message', 'Created At', 'IP Address'])
    for cm in comments:
        writer.writerow([cm.user_name,cm.message,cm.created_at,cm.ip_address.ip_address])

    return response

def moderate(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    cmod = ChannelMod.objects.filter(channel__channel_name = room_name)

    print(request.user)
    
    if cmod:
        cmod = cmod[0]
    print(cmod.users.all())
    if cmod and (request.user not in cmod.users.all()):
        print("Mismatched Permission Matrix")
        return render(request, 'comments/nopermission.html')
    return render(request, 'comments/room_mod.html', {
        'room_name': room_name
    })
