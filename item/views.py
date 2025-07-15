from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, Category
from .forms import NewItemForm, EditItemForm

def browse_items(request):
    """
    Display a list of unsold items, filtered by search query and category.
    """
    search_query = request.GET.get('search', '')
    selected_category_id = request.GET.get('category', 0)
    all_categories = Category.objects.all()
    unsold_items = Item.objects.filter(is_sold=False)

    if selected_category_id:
        unsold_items = unsold_items.filter(category_id=selected_category_id)

    if search_query:
        unsold_items = unsold_items.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    if not unsold_items.exists():
        messages.info(request, 'No items found matching your criteria.')

    return render(request, 'item/items.html', {
        'items': unsold_items,
        'search_query': search_query,
        'categories': all_categories,
        'selected_category_id': int(selected_category_id)
    })

def item_detail(request, pk):
    """
    Display detailed view of a specific item.
    """
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(
        category=item.category, 
        is_sold=False
    ).exclude(pk=pk)[0:3]
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def create_item(request):
    """
    Handle creation of new items.
    """
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()
            messages.success(request, 'Item created successfully!')
            return redirect('item:item_detail', pk=new_item.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Create New Item'
    })

@login_required
def delete_item(request, pk):
    """
    Handle item deletion.
    """
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    
    try:
        item.delete()
        messages.success(request, 'Item deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')
    
    return redirect('dashboard:index')

@login_required
def edit_item(request, pk):
    """
    Handle item editing.
    """
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item:item_detail', pk=item.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item'
    })