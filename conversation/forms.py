from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    """
    Form for creating or updating a conversation message with modern styling.
    """
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control modern-textarea',  # Added custom class
                'rows': 4,
                'placeholder': 'Type your message here...',
                'style': 'resize: none;',  # Disable textarea resizing
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Add Bootstrap and custom styling to the form.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control modern-input',  # Added custom class
            })