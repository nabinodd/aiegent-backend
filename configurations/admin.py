from django.contrib import admin

from .models import AllowedNumber


@admin.register(AllowedNumber)
class AllowedNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'created_at', 'updated_at', 'is_allowed')
    list_editable = ('is_allowed',)
    list_display_links = ('name', 'number', 'created_at', 'updated_at')
    search_fields = ('name', 'number')