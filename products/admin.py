from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('category', 'title', 'stock')
    ordering=('category', 'title')
    search_fields=('title',)
    fieldsets=(
        ('Products',{
            'fields':(
            ('category', 'title'), 'description',
            ('stock', 'price'),
            )
        }),
    )
