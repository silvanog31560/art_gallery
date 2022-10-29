from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.mail import send_mail
import stripe
from datetime import date
import datetime
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.decorators import permission_required
from django.conf import settings

from .models import UserItem
from products.models import Product
from products.views import UserAccessMixin
from accounts.models import ShippingAddress
from .extras import generate_order_id

# Create your views here.
@login_required()
def add_to_cart(request, **kwargs):
    item_qty = int(request.GET.get('item_qty'))
    # filter products by id
    item_id = kwargs.get('item_id')
    product = Product.objects.filter(id=item_id).first()

    # create orderItem of the selected product
    order_item, created = UserItem.objects.get_or_create(user_id=request.user.id,
                                                items=product, invoice='')
    if not created:
        messages.info(request, "Item already in cart.")
    else:
        if item_qty > product.stock:
            order_item.quantity=product.stock
            order_item.save()
            messages.success(request, f"{product.stock} added to cart!")
        else:
            order_item.quantity=item_qty
            order_item.save()
            messages.success(request, f"{item_qty} added to cart!")

    return redirect(reverse('products:product-detail', kwargs={'pk': item_id}))

@login_required()
def update_quantity(request, **kwargs):
    item_qty = int(request.GET.get('item_qty'))
    # filter products by id
    item_id = kwargs.get('item_id')
    product = Product.objects.filter(id=item_id).first()
    # update quantity of item in cart
    if item_qty > product.stock:
        UserItem.objects.filter(user_id=request.user.id,items=product, invoice='').update(quantity=product.stock)
        messages.success(request, f"Quantity updated to max stock of {product.stock}!")
    else:
        UserItem.objects.filter(user_id=request.user.id,items=product, invoice='').update(quantity=item_qty)
        messages.success(request, f"Quantity updated to {item_qty}!")

    return redirect(reverse('shopping_cart:order-summary'))

@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = UserItem.objects.get(pk=item_id)
    if item_to_delete:
        item_to_delete.delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order-summary'))

@login_required()
def order_details(request, **kwargs):
    existing_order = UserItem.objects.filter(user=request.user.id, invoice='').order_by('added')
    cart_total = "{0:.2f}".format(sum(float(item.total_price) for item in existing_order))

    #  template will use cart_user to determine if customer needs to enter shipping address
    try:
        cart_user = ShippingAddress.objects.get(user_id = request.user.id)
    except ObjectDoesNotExist:
        cart_user = None

    context = {
        'order': existing_order,
        'cart_total': cart_total,
        'cart_user': cart_user,
    }
    return render(request, 'cart/order_summary.html', context)

@login_required()
def checkout(request, **kwargs):
    existing_order =  UserItem.objects.filter(user=request.user.id, invoice='').order_by('added')
    cart_total = "{0:.2f}".format(sum(float(item.total_price) for item in existing_order))
    cart_user = ShippingAddress.objects.get(user_id = request.user.id)

    context = {
        'order': existing_order,
        'cart_total': cart_total,
        'cart_user': cart_user,
    }

    return render(request,'cart/checkout.html', context)

@login_required()
def success(request):
    session_id = request.GET.get('session_id')
    existing_order =  UserItem.objects.filter(user=request.user.id, invoice='').order_by('added')
    cart_total = "{0:.2f}".format(sum(float(item.total_price) for item in existing_order))
    customer = ShippingAddress.objects.get(user_id = request.user.id)
    product_detail = ""
    invoice_number = ""

    if session_id is None:
        return render(request,'art/index.html')
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = stripe_payment_intent=session.payment_status
    except:
        return render(request,'art/index.html')

    #  using existing_order in case user refreshes page to avoid running code again
    if payment_status == 'paid' and existing_order:
        invoice_number = generate_order_id()
        for item in existing_order:
            product = Product.objects.filter(id=item.items.id).get()
            order_item = UserItem.objects.filter(user_id=request.user.id, items=product, invoice='').get()

            product.stock-=order_item.quantity
            if product.category == 'DA':
                order_item.tracking_number = 'digital'
            product.save()
            order_item.invoice = invoice_number
            order_item.sold = datetime.datetime.now(tz=timezone.utc)
            order_item.save()
            product_detail += f"Qty:{order_item.quantity} Item:{order_item.items.title}\n"

        send_mail(
            subject="Invoice from Art",
            message=f"""Thank you for your purchase!
            Your reference number is: {invoice_number}
            Purchase details:
                {product_detail}
            Total price: ${cart_total}""",
            recipient_list=[request.user.email],
            from_email=settings.CONTACT_EMAIL,
        )

        send_mail(
            subject=f"New Order {invoice_number}",
            message=f"""
            Reference number: {invoice_number}
            Order details:
                {product_detail}
            Total price: ${cart_total}
            Name: {customer.first_name} {customer.last_name}
            Shipping Information:
            {customer.address}
            {customer.city}
            {customer.state}
            {customer.zip_code}
            {request.user.email}
            """,
            recipient_list=[settings.CONTACT_EMAIL],
            from_email=settings.CONTACT_EMAIL,
        )


    context={
        "session_id":session_id,
        "invoice":invoice_number,
    }

    return render(request,'cart/success.html', context)

class PendingOrderList(UserAccessMixin, ListView):
    permission_required = 'useritem.view_useritem'
    template_name = 'cart/pending_order_list.html'
    context_object_name = 'pending_items'
    queryset = UserItem.objects.exclude(invoice='').filter(tracking_number='')

@permission_required('useritem.change_useritem', raise_exception=True)
def pending_order_update(request, **kwargs):
    invoice_number = request.GET.get('invoice_number')
    pending_order = UserItem.objects.filter(invoice=invoice_number, tracking_number='')
    customer = ShippingAddress.objects.get(user_id=pending_order.first().user)

    if request.method == "POST":
        tracking = request.POST['tracking']
        UserItem.objects.filter(invoice=invoice_number).update(tracking_number=tracking)
        send_mail(
                subject=f"{invoice_number} Order Shipped",
                message=f"""
                Your order has shipped!
                Reference number: {invoice_number}
                Tracking number:{tracking}
                Thank you for your purchase! We appreciate your business.
                Please feel free to come back to WEBSITE and leave feedback and share
                your experience!
                """,
                recipient_list=[customer.user.email,],
                from_email=settings.CONTACT_EMAIL,
            )
        return redirect(reverse('shopping_cart:pending-orders'))

    context={
        "invoice_number":invoice_number,
        "pending_order":pending_order,
    }


    return render(request,'cart/pending_order_form.html', context)
