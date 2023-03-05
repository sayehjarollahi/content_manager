from django.shortcuts import render


def profile(request):
    return render(request, 'profile.html', context={
        'username': request.user.username,
        'date_joined': request.user.date_joined,
    })
