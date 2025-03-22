from django.db import models
from django.contrib.auth import get_user_model
from item.models import Item

User = get_user_model()

class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        # Display the conversation with the item name and participants
        participants = ", ".join([user.username for user in self.members.all()])
        return f"Conversation about {self.item.name} (Participants: {participants})"


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Conversation Message'
        verbose_name_plural = 'Conversation Messages'

    def __str__(self):
        # Display the message with the sender's username and a snippet of the content
        return f"Message by {self.created_by.username}: {self.content[:50]}..."  # Show first 50 characters of the message