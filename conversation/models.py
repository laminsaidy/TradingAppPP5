from django.db import models
from django.contrib.auth import get_user_model
from item.models import Item

User = get_user_model()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"



class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False, db_index=True)  

    class Meta:
        ordering = ('-modified_at',)
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        participants = ", ".join([user.username for user in self.members.all()])
        return f"Conversation about {self.item.name} ({participants})"

    def mark_as_read(self, user):
        """Mark all unread messages as read for a specific user"""
        self.messages.exclude(created_by=user).update(is_read=True)
        self.is_read = True
        self.save()

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)  

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Conversation Message'
        verbose_name_plural = 'Conversation Messages'

    def __str__(self):
        return f"Message by {self.created_by.username}: {self.content[:50]}..."