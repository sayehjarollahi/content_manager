from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import SignUpForm


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('signup')
    template_name = 'signup.html'
