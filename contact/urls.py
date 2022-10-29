from django.urls import path

from . import views

app_name='contact'
urlpatterns = [
    path('contact-us/', views.ContactForm.as_view(), name="contact-us"),

]
