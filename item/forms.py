from django import forms
from .models import Item, Category

INPUT_CLASSES = 'form-control py-3 px-4 rounded border'

class BaseItemForm(forms.ModelForm):
    """Base form with common methods for both item forms"""
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc) < 10:
            raise forms.ValidationError("Description must be at least 10 characters.")
        return desc

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Image file too large (max 2MB).")
            
            # More robust file type checking
            valid_content_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            content_type = getattr(image, 'content_type', None)
            
            if content_type is None:
                # Fallback check for some file upload scenarios
                if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    raise forms.ValidationError("Unsupported file type.")
            elif content_type not in valid_content_types:
                raise forms.ValidationError("Uploaded file is not a valid image.")
        return image

class NewItemForm(BaseItemForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"
        self.fields['category'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'id': 'category-select'
        })

    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }

class EditItemForm(BaseItemForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"
        self.fields['category'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'id': 'category-select'
        })

    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }