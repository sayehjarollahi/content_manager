from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import RegisterForm


# Sign Up View
class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('register')
    template_name = 'register.html'


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username,
    }

    return render(request, 'index.html', context=context)
