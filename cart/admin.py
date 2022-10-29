from django.contrib import admin
from .models import UserItem

@admin.register(UserItem)
class UserItemAdmin(admin.ModelAdmin):
    list_display=('items', 'user', 'invoice')
    ordering=('invoice',)
    search_fields=('invoice',)
    fieldsets=(
        ('Cart Items',{
            'fields':(
            'user', ('items', 'quantity'), 'invoice',
             'tracking_number',
            )
        }),
    )
