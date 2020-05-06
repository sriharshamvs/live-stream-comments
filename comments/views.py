from django.shortcuts import render

# Create your views here.

def room(request, room_name):
    return render(request, 'comments/room.html', {
        'room_name': room_name
    })


def moderate(request, room_name):
    return render(request, 'comments/room_mod.html', {
        'room_name': room_name
    })