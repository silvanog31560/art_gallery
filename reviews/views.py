from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Review
from accounts.models import CustomUser

class ReviewListview(ListView):
    model = Review
    context_object_name = 'review_list'
    paginate_by = 2

class ReviewCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Review
    fields = ('review',)
    success_url = reverse_lazy('reviews:reviews-list')

    def form_valid(self, form):
        form.instance.user = CustomUser.objects.get(username=self.request.user)
        return super().form_valid(form)

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Review
    fields = ('review',)
    context_object_name = 'review_update'
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('reviews:reviews-list')

class ReviewDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Review
    context_object_name = 'review_delete'
    success_url = reverse_lazy('reviews:reviews-list')
