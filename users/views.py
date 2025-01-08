from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users:registration_success')

    def form_valid(self, form):
        return super().form_valid(form)


class SuccessRegistrationView(TemplateView):
    template_name = 'user_success_registration.html'
