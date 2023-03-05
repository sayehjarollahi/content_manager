from django.shortcuts import render


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username,
    }

    return render(request, 'index.html', context=context)
