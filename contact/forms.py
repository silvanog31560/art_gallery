from django.forms import ModelForm
from .models import Contact
from django import forms

class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
          'message': forms.Textarea(attrs={'rows':6, 'cols':30}),
        }
