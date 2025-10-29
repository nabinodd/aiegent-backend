from django.contrib import admin
from .models import AllowedNumber

@admin.register(AllowedNumber)
class AllowedNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'created_at', 'updated_at')
    list_display_links = list_display
    search_fields = ('name', 'number')