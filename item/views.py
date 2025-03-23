from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
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

    # Filter items by selected category
    if selected_category_id:
        unsold_items = unsold_items.filter(category_id=selected_category_id)

    # Filter items by search query
    if search_query:
        unsold_items = unsold_items.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'item/items.html', {
        'items': unsold_items,
        'search_query': search_query,
        'categories': all_categories,
        'selected_category_id': int(selected_category_id)
    })

# Other view functions (e.g., detail, create_item, EditButton, DeleteButton)
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def create_item(request):
    """
    Allows a logged-in user to create a new item.
    Redirects to the item's detail page after successful creation.
    """
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        # Validate the form
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()
            return redirect('item:detail', pk=new_item.id)
    else:
        form = NewItemForm()

    # Render the form template with the form and a custom title
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Create a New Item',  
    })

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

        form = EditItemForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            updated_item = form.save(commit=False)  
            updated_item.save() 
            return redirect('item:detail', pk=updated_item.id)  
    else:
        form = EditItemForm(instance=product)

    # Render the form template with the form and a custom title
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Modify Item Details',  
    })