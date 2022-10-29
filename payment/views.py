import stripe
from django.views import View
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from cart.models import UserItem
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):

    def post(self, request,  *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        existing_order =  UserItem.objects.filter(user=request.user.id, invoice="")
        stripe_total = sum(item.stripe_price for item in existing_order)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                      'currency': 'usd',
                      'unit_amount': stripe_total,
                      'product_data': {
                        'name': "Aryanna's Art",
                        'description': "Arts and crafts",
                      },
                    },
                    'quantity': 1,
                  }],
                metadata={
                        "existing_order": existing_order
                },
                mode='payment',
                success_url=YOUR_DOMAIN + 'cart/purchase-success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + 'cart/order-summary/',
            )

        except Exception as e:
            return str(e)

        return redirect(checkout_session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        customer_name = session["customer_details"]["name"]
        paid_order = session["metadata"]["existing_order"]
        amount_total = str(session["amount_total"])
        amount_total = amount_total[:-2]+"."+amount_total[-2:]
        # print(session)

        send_mail(
            subject="Payment Confirmation",
            message=f"""
            Customer's Name: {customer_name}
            Customer's Email: {customer_email}
            Order:
            {paid_order}
            Total:${amount_total}
            """,
            recipient_list=[settings.CONTACT_EMAIL],
            from_email=settings.CONTACT_EMAIL,
        )

    # Passed signature verification
    return HttpResponse(status=200)
