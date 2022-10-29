from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

from .models import Product
from .forms import ProductForm

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),
                                    self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('home')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)

class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'
    paginate_by = 6

    def get_queryset(self):
        # captured from url
        filter_val = self.kwargs['filter_val']
        order = self.kwargs['orderby']

        if order == 'price' or order == '-price':
            # exclude not for sale
            ProductForSale = Product.objects.exclude(stock=0)
            new_context = ProductForSale.filter(category=filter_val,
            ).order_by(order)
        elif order == '-added':
            # exclude not for sale
            ProductForSale = Product.objects.exclude(stock=0)
            new_context = ProductForSale.filter(category=filter_val,
            ).order_by(order)
        else:
            #  returns all
            new_context = Product.objects.filter(category=filter_val,
            ).order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['filter'] = self.kwargs['filter_val']
        context['orderby'] = self.kwargs['orderby']
        return context

class ProductCreate(UserAccessMixin, CreateView):
    permission_required = 'product.add_product'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('home')

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product_detail'

class ProductUpdate(UserAccessMixin, UpdateView):
    permission_required = 'product.change_product'
    model = Product
    context_object_name = 'product_update'
    template_name_suffix = "_update_form"
    fields = ('title', 'description', 'category',
    'stock', 'price')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('products:product-detail', kwargs={'pk': pk})

class ProductDelete(UserAccessMixin, DeleteView):
    permission_required = 'product.delete_product'
    model = Product
    context_object_name = 'product_delete'
    success_url = reverse_lazy('home')
