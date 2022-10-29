from django.shortcuts import render
from django.views.generic import FormView
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm




class ContactForm(FormView):
    form_class = ContactForm
    success_url = '?submitted=True'
    template_name = 'contact/contact.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

    def form_valid(self,form):
        form.save()
        cd = form.cleaned_data
        email_subject=f"From: {cd['email']}; Subject: {cd['subject']}"
        email_message=cd['message']
        send_mail(
            email_subject,
            email_message,
            settings.CONTACT_EMAIL,
            [settings.CONTACT_EMAIL]
        )
        return super().form_valid(form)
