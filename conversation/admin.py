from django.contrib import admin
from .models import Conversation, ConversationMessage

from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'responded')
    list_filter = ('is_read', 'responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'responded')
    date_hierarchy = 'created_at'
    actions = ['mark_as_responded', 'send_response']
    
    def send_response(self, request, queryset):
        for message in queryset:
            send_mail(
                f"Re: {message.subject}",
                "Thank you for your message...",
                settings.DEFAULT_FROM_EMAIL,
                [message.email],
                fail_silently=False,
            )
            message.responded = True
            message.save()
        self.message_user(request, "Responses sent successfully")
    send_response.short_description = "Send email response to selected messages"


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'get_participants', 'created_at', 'modified_at')
    list_filter = ('created_at', 'modified_at')
    search_fields = ('item__name', 'members__username')
    filter_horizontal = ('members',)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.members.all()])
    get_participants.short_description = 'Participants'

@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'created_by', 'content_snippet', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('content', 'created_by__username', 'conversation__item__name')

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'