from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation

from .forms import ContactForm
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:contact_thanks')
    else:
        form = ContactForm()
    return render(request, 'products/contact.html', {'form': form})

def contact_thanks(request):
    return render(request, 'products/contact_thanks.html')


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user).prefetch_related(
        'members', 
        'item',
        'messages'
    ).order_by('-modified_at')
    
    # Count unread conversations
    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(created_by=request.user).count()
    
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
        'unread_count': sum(conv.unread_count for conv in conversations)
    })

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    existing_conv = Conversation.objects.filter(
        item=item,
        members=request.user
    ).first()
    
    if existing_conv:
        return redirect('conversation:detail', pk=existing_conv.id)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user, item.created_by)
            
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            
            return redirect('conversation:detail', pk=conversation.id)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item
    })

@login_required
def detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('messages', 'members'),
        pk=pk,
        members=request.user
    )
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
            
            conversation.modified_at = message.created_at
            conversation.save()
            
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()
    
    # Mark messages as read
    conversation.mark_as_read(request.user)
    
    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
        'other_user': conversation.members.exclude(id=request.user.id).first()
    })