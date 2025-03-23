from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewItemForm, EditItemForm  
from .models import Item

@login_required
def create_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()
            return redirect('item:detail', pk=new_item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Create a New Item',
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

def items(request):
    items_list = Item.objects.filter(is_sold=False)
    return render(request, 'item/items.html', {'items': items_list})

@login_required
def DeleteButton(request, pk):
    """
    Deletes an item if the logged-in user is the creator.
    Redirects to the dashboard after deletion.
    """
    # Fetch the item, ensuring it belongs to the logged-in user
    product = get_object_or_404(Item, pk=pk, created_by=request.user)

    product.delete()

    return redirect('dashboard:index')

@login_required
def EditButton(request, pk):
    """
    Allows the logged-in user to edit an item they created.
    Redirects to the item's detail page after successful update.
    """
    # Fetch the item, ensuring it belongs to the logged-in user
    product = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        # Populate the form with the submitted data and files
        form = EditItemForm(request.POST, request.FILES, instance=product)

        # Validate and save the form if it's valid
        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.save()  
            return redirect('item:detail', pk=updated_item.id)
          
        form = EditItemForm(instance=product)

    # Render the form template with the form and a custom title
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Modify Item Details',  
    })