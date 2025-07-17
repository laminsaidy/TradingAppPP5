from django import forms
from .models import Item, Category
import cloudinary

INPUT_CLASSES = 'form-control py-3 px-4 rounded border'

class BaseItemForm(forms.ModelForm):
    """Base form with common methods for both item forms"""
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"
        self.fields['category'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'id': 'category-select'
        })
        self.fields['name'].widget.attrs.update({'class': INPUT_CLASSES})
        self.fields['description'].widget.attrs.update({'class': INPUT_CLASSES})
        self.fields['price'].widget.attrs.update({'class': INPUT_CLASSES})
        self.fields['image'].widget.attrs.update({'class': INPUT_CLASSES})

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
        if image and hasattr(image, 'file'):  # Only for new uploads
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError("Image file too large (max 2MB).")
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Uploaded file is not an image.")
        return image

class NewItemForm(BaseItemForm):
    pass

class EditItemForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        fields = BaseItemForm.Meta.fields + ('is_sold',)