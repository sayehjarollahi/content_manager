from django.shortcuts import redirect


def redirect_not_authenticated(request):
    if not request.user.is_authenticated:
        return redirect('/')
