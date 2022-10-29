from django import forms
from products.models import Product
from django import forms

class ProductForm(forms.ModelForm):

    class Meta():
        model = Product
        fields = (
            'title', 'description', 'category',
            'stock', 'price', 'landscape', 'portrait',
            'wm_landscape', 'wm_portrait',
            )
        widgets = {
            'price':forms.TextInput(),
            'description': forms.Textarea(attrs={'rows':6, 'cols':47}),
        }

    def clean(self):
        cleaned_data = super().clean()
        landscape = cleaned_data.get("landscape")
        portrait = cleaned_data.get("portrait")
        wm_landscape = cleaned_data.get("wm_landscape")
        wm_portrait = cleaned_data.get("wm_portrait")
        if not (landscape or portrait or wm_landscape or wm_portrait):
            raise forms.ValidationError(
            "You must choose an image."
            )
        if landscape and portrait or landscape and wm_landscape or landscape and wm_portrait:
            raise forms.ValidationError(
            "You must choose only one image at a time."
            )
        if portrait and wm_landscape or portrait and wm_portrait or wm_portrait and wm_landscape:
            raise forms.ValidationError(
            "You must choose only one image at a time."
            )
