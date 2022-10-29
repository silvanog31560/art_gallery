from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ShippingAddress

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    ordering = ('username',)
    search_fields = ('username',)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name')
    ordering=('last_name', 'first_name')
    search_fields=('first_name', 'last_name')
    fieldsets=(
        ('Shipping Information',{
            'fields':(
            'user', ('first_name', 'last_name'), 'address',
            ('city', 'state',), 'zip_code',
            )
        }),
    )
