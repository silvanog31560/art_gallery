from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

from .models import CustomUser, ShippingAddress
from .forms import CustomUserCreationForm, CustomUserChangeForm, ShippingAddressForm

# Create your views here.
class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    success_url = reverse_lazy('home')
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name_suffix = '_update_form'

    # override to avoid passing pk in url
    # uses self.request.user to track user
    def get_object(self, *args, **kwargs):
        return CustomUser.objects.get(username = self.request.user)

class ShippingAddressCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    success_url = reverse_lazy('shopping_cart:order-summary')
    model = ShippingAddress
    form_class = ShippingAddressForm

    # To track the user that created an object
    #  OneToOneField with CustomUser
    def form_valid(self, form):
        form.instance.user = CustomUser.objects.get(username=self.request.user)
        return super().form_valid(form)

class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    success_url = reverse_lazy('shopping_cart:checkout')
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name_suffix = '_update_form'

    # override to avoid passing pk in url
    # uses self.request.user to track user
    def get_object(self, *args, **kwargs):
        user = CustomUser.objects.get(username = self.request.user)
        # uses user variable to access id linked to CustomUser
        # in case pk is not in sink
        return ShippingAddress.objects.get(user_id = user.id)
