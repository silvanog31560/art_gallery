from django.urls import path

from .views import Register, CustomUserUpdateView, ShippingAddressCreateView, ShippingAddressUpdateView

app_name='accounts'
urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("shipping-address/",
        ShippingAddressCreateView.as_view(), name="shipping-address"),
    path("edit-shipping-address/",
        ShippingAddressUpdateView.as_view(), name="edit-shipping-address"),
    path("update-user",
        CustomUserUpdateView.as_view(), name="update-user")
]
