from django.contrib import admin
from .models import Conversation, ConversationMessage

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