from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = (
        "role",
        "content",
        "created_at",
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "session_id",
        "created_at",
    )

    search_fields = (
        "session_id",
    )

    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "conversation",
        "role",
        "created_at",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "content",
    )