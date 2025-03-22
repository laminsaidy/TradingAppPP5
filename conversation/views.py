from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item  
from .forms import ConversationMessageForm  
from .models import Conversation  

def inbox(request):
    """
    Render the inbox page for conversations.
    """
    return render(request, 'conversation/inbox.html')

def new_conversation(request, item_pk):  
    """
    Start a new conversation about a specific item.
    """
    # Fetch the item or return a 404 error if it doesn't exist
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
        # Render an empty form for GET requests
        form = ConversationMessageForm()  
    
    # Render the new conversation template with the form
    return render(request, 'conversation/new.html', {
        'form': form
    })