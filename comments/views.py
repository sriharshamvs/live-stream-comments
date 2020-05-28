from django.shortcuts import render, redirect

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

def moderate(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    return render(request, 'comments/room_mod.html', {
        'room_name': room_name
    })
