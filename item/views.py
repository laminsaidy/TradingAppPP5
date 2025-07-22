# item views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Item, Category
from .forms import NewItemForm, EditItemForm
import cloudinary.uploader

def browse_items(request):
    """
    Display a list of unsold items, filtered by search query and category.
    """
    search_query = request.GET.get('search', '')
    selected_category_id = request.GET.get('category', 0)
    all_categories = Category.objects.all()
    unsold_items = Item.objects.filter(is_sold=False).select_related('category', 'created_by')

    if selected_category_id:
        unsold_items = unsold_items.filter(category_id=selected_category_id)

    if search_query:
        unsold_items = unsold_items.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).distinct()

    context = {
        'items': unsold_items,
        'search_query': search_query,
        'categories': all_categories,
        'selected_category_id': int(selected_category_id)
    }

    if not unsold_items.exists():
        messages.info(request, 'No items found matching your criteria.')

    return render(request, 'item/items.html', context)

def item_detail(request, pk):
    """
    Display detailed view of a specific item.
    """
    item = get_object_or_404(Item.objects.select_related('created_by', 'category'), pk=pk)
    related_items = Item.objects.filter(
        category=item.category, 
        is_sold=False
    ).exclude(pk=pk).select_related('created_by')[:3]
    
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
            try:
                new_item = form.save(commit=False)
                new_item.created_by = request.user
                
                # Handle Cloudinary upload if needed
                if 'image' in request.FILES:
                    upload_result = cloudinary.uploader.upload(request.FILES['image'])
                    new_item.image = upload_result['secure_url']
                
                new_item.save()
                messages.success(request, 'Item created successfully!')
                return redirect('item:item_detail', pk=new_item.id)
            except Exception as e:
                messages.error(request, f'Error creating item: {str(e)}')
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
    Handle item deletion with Cloudinary cleanup.
    """
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    
    try:
        # Optional: Delete image from Cloudinary if needed
        if item.image and hasattr(item.image, 'public_id'):
            cloudinary.uploader.destroy(item.image.public_id)
        
        item.delete()
        messages.success(request, 'Item deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting item: {str(e)}')
    
    return redirect('dashboard:index')

@login_required
def edit_item(request, pk):
    """
    Handle item editing with Cloudinary support.
    """
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                # Handle Cloudinary upload if new image is provided
                if 'image' in request.FILES:
                    # Optional: Delete old image from Cloudinary if needed
                    if item.image and hasattr(item.image, 'public_id'):
                        cloudinary.uploader.destroy(item.image.public_id)
                    
                    upload_result = cloudinary.uploader.upload(request.FILES['image'])
                    item.image = upload_result['secure_url']
                
                form.save()
                messages.success(request, 'Item updated successfully!')
                return redirect('item:item_detail', pk=item.id)
            except Exception as e:
                messages.error(request, f'Error updating item: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item'
    })