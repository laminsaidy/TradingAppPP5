from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def inbox(request):
    """
    Render the inbox page with conversations for the logged-in user.
    """
    # Fetch conversations where the current user is a member
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def new_conversation(request, item_pk):
    """
    Handle starting a new conversation about a specific item.
    """
    item = get_object_or_404(Item, pk=item_pk)

    # Prevent the item creator from starting a conversation with themselves
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # Check if a conversation already exists between the current user and the item creator
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # Redirect to the existing conversation if one is found
    if conversations.exists():
        return redirect('conversation:detail', pk=conversations.first().id)

    # Handle form submission
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Create a new conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Save the conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Redirect to the item detail page
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    # Render the new conversation template with the form
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def detail(request, pk):
    """
    Render the conversation detail page with messages.
    """
    # Fetch the conversation where the current user is a member
    conversation = get_object_or_404(Conversation, members__in=[request.user.id], pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })