from django import forms
from .models import Item

from django import forms
from .models import Item

from .models import Item, Category  

INPUT_CLASSES = 'form-control py-3 px-4 rounded border'

class NewItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly load categories and customize the field
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"  # Replace "------"
        self.fields['category'].widget.attrs.update({
            'class': INPUT_CLASSES,
            'id': 'category-select'  
        })

    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            # Note: 'category' is now handled in __init__
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),  
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }