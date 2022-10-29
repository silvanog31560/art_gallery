from django.urls import path
from . import views
from .views import (
    add_to_cart,
    update_quantity,
    delete_from_cart,
    order_details,
    checkout,
    success,
    pending_order_update
)

app_name = 'shopping_cart'
urlpatterns = [
    path("add-to-cart/?<item_id>/", add_to_cart, name="add_to_cart"),
    path("update-quantity/?<item_id>/", update_quantity, name="update-quantity"),
    path("order-summary/", order_details, name="order-summary"),
    path("item/delete/?<item_id>", delete_from_cart, name="delete_from_cart"),
    path("checkout/", checkout, name="checkout"),
    path("purchase-success/", success,
        name="purchase-success"),
    path("pending-orders/", views.PendingOrderList.as_view(), name="pending-orders"),
    path("update-pending-orders/", pending_order_update, name="update-pending-orders"),
]
