from django.shortcuts import render

from account.views.utils import redirect_not_authenticated


def profile(request):
    auth_result = redirect_not_authenticated(request)
    if auth_result is not None:
        return auth_result

    return render(request, 'profile.html', context={
        'username': request.user.username,
        'date_joined': request.user.date_joined,
    })
