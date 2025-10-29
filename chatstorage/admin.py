from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'created_at')
    list_display_links = list_display
    readonly_fields = ('id', 'sender', 'message', 'created_at', 'updated_at')
    search_fields = ('sender',)
    ordering = ('-created_at',)
    list_filter = ('sender',)