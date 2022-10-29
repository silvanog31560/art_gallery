from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('user', 'created')
    ordering=('user', 'review')
    search_fields=('user',)
    fieldsets=(
        ('Reviews',{
            'fields':(
            'user', 'review',
            )
        }),
    )
