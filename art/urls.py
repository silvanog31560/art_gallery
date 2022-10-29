"""art URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from payment.views import CreateCheckoutSessionView, stripe_webhook

admin.site.site_header = "Aryanna's Site Administration"
admin.site.site_title = "Aryanna's Site Admin"
admin.site.index_title = "Aryanna's Site Admin Home" 


urlpatterns = [
    path("", TemplateView.as_view(template_name="art/index.html"), name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('success/', TemplateView.as_view(template_name="registration/success.html"),
        name="register-success"),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='shopping_cart')),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(),
        name='create-checkout-session'),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('contact/', include('contact.urls', namespace='contact'))
]
